// WealthGlobe — tiny proxy + static server.
// Why a server at all? The fun data sources (GDELT news, Yahoo Finance quotes,
// the world borders GeoJSON) either block browser CORS or are noisy to hit
// directly. We proxy them here so the frontend stays key-free and CORS-free.

const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');
const GEOJSON_CACHE = path.join(PUBLIC_DIR, 'data', 'countries.geojson');

app.use(express.static(PUBLIC_DIR));

// --- tiny in-memory cache so we're polite to the upstream APIs -------------
// Each entry carries its own TTL, so we can keep good results long but expire
// rate-limited fallbacks fast (lets the app self-heal once GDELT recovers).
const cache = new Map();
function cacheGet(key) {
  const hit = cache.get(key);
  if (hit && Date.now() - hit.t < hit.ttl) return hit.v;
  return null;
}
function cacheSet(key, v, ttl) {
  cache.set(key, { t: Date.now(), v, ttl });
  return v;
}
function memo(key, ttlMs, producer) {
  const hit = cacheGet(key);
  if (hit) return Promise.resolve(hit);
  return producer().then((v) => cacheSet(key, v, ttlMs));
}

const UA = { 'User-Agent': 'Mozilla/5.0 (WealthGlobe demo)' };

async function fetchJson(url, opts = {}) {
  const res = await fetch(url, { headers: UA, ...opts });
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Non-JSON from ${url}: ${text.slice(0, 120)}`);
  }
}

// --- world borders (cached to disk after first fetch -> works offline) -----
const GEOJSON_SOURCES = [
  'https://raw.githubusercontent.com/vasturiano/globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson',
  'https://vasturiano.github.io/globe.gl/example/datasets/ne_110m_admin_0_countries.geojson',
];

app.get('/api/geojson', async (req, res) => {
  try {
    if (fs.existsSync(GEOJSON_CACHE)) {
      return res.type('application/json').send(fs.readFileSync(GEOJSON_CACHE, 'utf8'));
    }
    let lastErr;
    for (const url of GEOJSON_SOURCES) {
      try {
        const r = await fetch(url, { headers: UA });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const body = await r.text();
        JSON.parse(body); // validate
        fs.writeFileSync(GEOJSON_CACHE, body);
        return res.type('application/json').send(body);
      } catch (e) {
        lastErr = e;
      }
    }
    throw lastErr || new Error('no geojson source');
  } catch (e) {
    res.status(502).json({ error: 'geojson unavailable', detail: String(e) });
  }
});

// --- news: GDELT (no key, global) with a Hacker News fallback --------------
function gdeltQuery(q) {
  const clean = String(q || '').trim().replace(/[()"]/g, '');
  // GDELT wants multi-word phrases quoted.
  return clean.includes(' ') ? `"${clean}"` : clean;
}

async function newsFromGdelt(q) {
  const query = encodeURIComponent(`${gdeltQuery(q)} sourcelang:english`);
  const url = `https://api.gdeltproject.org/api/v2/doc/doc?query=${query}&mode=ArtList&maxrecords=18&sort=DateDesc&format=json`;
  const data = await fetchJson(url);
  return (data.articles || []).map((a) => ({
    title: a.title,
    url: a.url,
    source: a.domain,
    date: a.seendate,
    image: a.socialimage || null,
  }));
}

async function newsFromHN(q) {
  const url = `https://hn.algolia.com/api/v1/search_by_date?query=${encodeURIComponent(q)}&tags=story&hitsPerPage=15`;
  const data = await fetchJson(url);
  return (data.hits || []).map((h) => ({
    title: h.title,
    url: h.url || `https://news.ycombinator.com/item?id=${h.objectID}`,
    source: 'Hacker News',
    date: h.created_at,
    image: null,
  }));
}

app.get('/api/news', async (req, res) => {
  const q = req.query.q;
  if (!q) return res.status(400).json({ error: 'missing q' });
  try {
    const key = `news:${q}`;
    let articles = cacheGet(key);
    if (!articles) {
      let arts = [];
      let goodSource = false; // true only when GDELT (the rich source) answered
      try {
        arts = await newsFromGdelt(q);
        goodSource = arts.length > 0;
      } catch {
        /* throttled or down -> fall through to HN */
      }
      if (!arts.length) {
        try {
          arts = await newsFromHN(q);
        } catch {
          /* fall through */
        }
      }
      // keep good results 5 min; expire fallbacks/empties in 45 s so we recover
      articles = cacheSet(key, arts, goodSource ? 5 * 60 * 1000 : 45 * 1000);
    }
    res.json({ q, articles });
  } catch (e) {
    res.status(502).json({ error: 'news unavailable', detail: String(e) });
  }
});

// --- the retention hook: a live business-headlines ticker ------------------
app.get('/api/headlines', async (req, res) => {
  try {
    const articles = await memo('headlines', 5 * 60 * 1000, async () => {
      try {
        return await newsFromGdelt('stock market OR earnings OR economy');
      } catch {
        return await newsFromHN('stock market');
      }
    });
    res.json({ articles });
  } catch (e) {
    res.status(502).json({ error: 'headlines unavailable', detail: String(e) });
  }
});

// --- stock: Yahoo Finance chart endpoint (no key, works server-side) -------
app.get('/api/quote', async (req, res) => {
  const symbol = req.query.symbol;
  if (!symbol) return res.status(400).json({ error: 'missing symbol' });
  try {
    const out = await memo(`quote:${symbol}`, 2 * 60 * 1000, async () => {
      const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(
        symbol
      )}?range=1mo&interval=1d`;
      const data = await fetchJson(url);
      const r = data?.chart?.result?.[0];
      if (!r) throw new Error('no result');
      const meta = r.meta || {};
      const closes = (r.indicators?.quote?.[0]?.close || []).filter((x) => x != null);
      const price = meta.regularMarketPrice ?? closes[closes.length - 1] ?? null;
      const prev = meta.chartPreviousClose ?? meta.previousClose ?? closes[0] ?? null;
      const change = price != null && prev ? ((price - prev) / prev) * 100 : null;
      return {
        symbol,
        price,
        currency: meta.currency || 'USD',
        changePct: change,
        spark: closes.slice(-30),
      };
    });
    res.json(out);
  } catch (e) {
    res.status(502).json({ error: 'quote unavailable', detail: String(e) });
  }
});

app.listen(PORT, () => {
  console.log(`\n  🌍 WealthGlobe running at  http://localhost:${PORT}\n`);
});
