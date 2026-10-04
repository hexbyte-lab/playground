/* WealthGlobe — a tactile money map.
 * Core loop: spin the globe -> pick a lens -> watch wealth light up ->
 * click a hotspot -> read live news + stock -> drill back out. */

(() => {
  'use strict';

  const SECTOR_COLORS = {
    Technology: '#6bd6ff',
    Financials: '#9b8cff',
    Healthcare: '#7bffb0',
    Energy: '#ffb84d',
    Consumer: '#ff8fcf',
    Industrials: '#cfd4dd',
    Materials: '#d6a86b',
  };

  const SECTORS = Object.keys(SECTOR_COLORS);

  let world;
  let companies = [];
  let byCountry = {}; // country -> { total, companies[] } (filtered to active sectors)
  let countriesGeo = null;
  let currentLens = 'companies';
  let maxCap = 1;
  const activeSectors = new Set(SECTORS); // industry filter — all on by default

  // ---------- helpers ----------
  const $ = (sel) => document.querySelector(sel);
  const fmtCap = (b) => (b >= 1000 ? `$${(b / 1000).toFixed(2)}T` : `$${b}B`);

  // red "heat" ramp from a 0..1 value, on a black base (dark-red -> orange -> white-hot)
  function heat(t) {
    t = Math.max(0, Math.min(1, t));
    const r = Math.round(70 + t * 185);
    const g = Math.round(Math.pow(t, 1.4) * 175);
    const b = Math.round(Math.max(0, t - 0.78) * 4 * 200);
    return `rgb(${r},${g},${b})`;
  }
  // radar heatmap color: same red ramp but with alpha so cold areas stay see-through
  function radarColor(t) {
    t = Math.max(0, Math.min(1, t));
    const a = Math.min(1, Math.pow(t, 0.7) * 1.5);
    const r = 255;
    const g = Math.round(Math.pow(t, 1.3) * 205);
    const b = Math.round(Math.max(0, t - 0.8) * 5 * 200);
    return `rgba(${r},${g},${b},${a})`;
  }
  // build a transparent->sector-color->white heat ramp for any sector hue
  const hexToRgb = (hex) => {
    const n = parseInt(hex.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  };
  function sectorRamp(sector) {
    const [r, g, b] = hexToRgb(SECTOR_COLORS[sector] || '#ffffff');
    return (t) => {
      t = Math.max(0, Math.min(1, t));
      // cap alpha lower (0.55 max) so 7 stacked sector shells don't compound into a blur
      const a = Math.min(0.55, Math.pow(t, 0.85) * 0.9);
      const w = Math.max(0, t - 0.7) * 3; // whiten toward the hot core
      const mix = (c) => Math.round(c + (255 - c) * w);
      return `rgba(${mix(r)},${mix(g)},${mix(b)},${a})`;
    };
  }
  // log scaling so giants don't drown everyone else
  const norm = (cap) => Math.log10(cap + 1) / Math.log10(maxCap + 1);

  // ---------- filtering / aggregation ----------
  const visibleCompanies = () => companies.filter((c) => activeSectors.has(c.sector));
  function rebuildAggregates() {
    const vis = visibleCompanies();
    byCountry = {};
    for (const c of vis) {
      (byCountry[c.country] ||= { total: 0, companies: [] });
      byCountry[c.country].total += c.cap;
      byCountry[c.country].companies.push(c);
    }
    for (const k in byCountry) byCountry[k].companies.sort((a, b) => b.cap - a.cap);
  }

  // ---------- data ----------
  async function loadData() {
    companies = await fetch('data/companies.json').then((r) => r.json());
    maxCap = Math.max(...companies.map((c) => c.cap));
    rebuildAggregates();

    try {
      const geo = await fetch('/api/geojson').then((r) => (r.ok ? r.json() : null));
      countriesGeo = geo && geo.features ? geo.features : null;
    } catch {
      countriesGeo = null;
    }
  }

  // ---------- globe ----------
  function initGlobe() {
    world = Globe()(document.getElementById('globeViz'))
      .backgroundColor('#000000')
      .showGlobe(true)
      .showGraticules(false)
      .showAtmosphere(true)
      .atmosphereColor('#ff6b5a')
      .atmosphereAltitude(0.16)
      // stationary heat shell sitting ABOVE the countries (base==top -> flat)
      // weight = market cap, so heat strength tracks how much wealth is there
      .heatmapsData([visibleCompanies()])
      .heatmapPointLat('lat')
      .heatmapPointLng('lng')
      .heatmapPointWeight((d) => d.cap)
      .heatmapBandwidth(3)
      .heatmapColorFn(() => radarColor) // accessor returns the interpolator
      .heatmapColorSaturation(1.5)
      .heatmapBaseAltitude(0.001)  // painted right on the sphere surface
      .heatmapTopAltitude(0.001)
      .heatmapsTransitionDuration(0)
      // blips float above the heat and the country outlines
      .pointsData(visibleCompanies())
      .pointLat('lat')
      .pointLng('lng')
      .pointAltitude(0.04)
      .pointRadius(0.26)
      .pointColor(pointColor)
      .pointResolution(6)
      .pointLabel(pointTip)
      .onPointClick(openCompany);

    // dark monochrome sphere
    const mat = world.globeMaterial();
    mat.color.set('#0a0a0e');
    mat.emissive.set('#0a0a0e');
    mat.shininess = 6;

    // polygons (country choropleth) — only if borders loaded
    if (countriesGeo) {
      world
        .polygonsData(countriesGeo)
        .polygonCapColor(countryCap)
        .polygonSideColor(() => 'rgba(0,0,0,0)')
        .polygonStrokeColor(() => 'rgba(255,255,255,0.55)')
        .polygonAltitude(countryAltitude)
        .polygonLabel(countryTip)
        .onPolygonClick((d) => openCountry(adminName(d)));
    }

    // tactile: gentle auto-spin that yields to the user
    const controls = world.controls();
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.45;
    controls.enableDamping = true;
    controls.dampingFactor = 0.12;
    const pause = () => (controls.autoRotate = false);
    document.getElementById('globeViz').addEventListener('pointerdown', pause);

    world.pointOfView({ lat: 25, lng: 10, altitude: 2.4 }, 0);
    window.addEventListener('resize', () => {
      world.width(window.innerWidth).height(window.innerHeight);
    });

    applyLens('companies');
  }

  // ---------- lens-dependent accessors ----------
  function pointColor(d) {
    if (currentLens === 'sector') return SECTOR_COLORS[d.sector] || '#ffffff';
    if (currentLens === 'countries') return 'rgba(255,255,255,0.18)';
    return 'rgba(255,255,255,0.7)'; // companies lens: white blips in the red heat
  }
  function pointTip(d) {
    const sw = SECTOR_COLORS[d.sector] || '#fff';
    return `<div class="globe-tip"><b>${d.name}</b> · ${d.ticker}<br>
      <span class="t-sub">${d.city}, ${d.country}</span><br>
      ${fmtCap(d.cap)} · <span style="color:${sw}">${d.sector}</span></div>`;
  }

  function adminName(feat) {
    const p = feat.properties || {};
    return p.ADMIN || p.NAME || p.name || '';
  }
  function countryCap(feat) {
    // outside the country lens, leave fills clear so the red heat glows through
    if (currentLens !== 'countries') return 'rgba(0,0,0,0)';
    const c = byCountry[adminName(feat)];
    if (!c) return 'rgba(18,18,22,0.55)';
    const maxC = Math.max(...Object.values(byCountry).map((x) => x.total));
    return heat(0.25 + (Math.log10(c.total + 1) / Math.log10(maxC + 1)) * 0.75);
  }
  // polygons float above the heat layer (0.001) so their outlines are always visible
  function countryAltitude() {
    return 0.012;
  }
  function countryTip(feat) {
    const name = adminName(feat);
    const c = byCountry[name];
    if (!c) return `<div class="globe-tip"><b>${name}</b><br><span class="t-sub">no tracked HQs</span></div>`;
    return `<div class="globe-tip"><b>${name}</b><br>
      ${fmtCap(c.total)} across ${c.companies.length} firms<br>
      <span class="t-sub">click to drill in</span></div>`;
  }

  function applyLens(lens) {
    currentLens = lens;
    document.querySelectorAll('.lens').forEach((b) =>
      b.classList.toggle('active', b.dataset.lens === lens)
    );

    const vis = visibleCompanies();
    if (lens === 'sector') {
      // one separately-coloured heat shell per active industry —
      // narrower bandwidth + lower saturation so stacked shells don't blur together
      const groups = [...activeSectors]
        .map((sec) => {
          const arr = vis.filter((c) => c.sector === sec);
          arr.sector = sec;
          return arr;
        })
        .filter((g) => g.length);
      world
        .heatmapBandwidth(1.8)
        .heatmapColorSaturation(1.0)
        .heatmapsData(groups)
        .heatmapColorFn((hm) => sectorRamp(hm.sector));
    } else if (lens === 'companies') {
      world
        .heatmapBandwidth(3)
        .heatmapColorSaturation(1.5)
        .heatmapsData(vis.length ? [vis] : [])
        .heatmapColorFn(() => radarColor);
    } else {
      world.heatmapsData([]); // countries lens uses the choropleth instead
    }

    world.pointColor(pointColor).pointsData(vis);
    if (countriesGeo) {
      world.polygonCapColor(countryCap).polygonsData(countriesGeo);
    }
    renderLegend(lens);
  }

  function renderLegend(lens) {
    const el = $('#legend');
    if (lens === 'sector') {
      el.innerHTML = `<div class="row"><span class="sw" style="background:${SECTOR_COLORS.Technology}"></span>each colour = an industry</div>
        <div class="row"><span class="sw" style="background:rgba(255,255,255,0.6)"></span>toggle them in the filter above</div>`;
    } else if (lens === 'countries') {
      el.innerHTML = `<div class="row"><span class="sw" style="background:${heat(
        0.95
      )}"></span>more corporate wealth</div>
        <div class="row"><span class="sw" style="background:${heat(
          0.3
        )}"></span>less</div>`;
    } else {
      el.innerHTML = `<div class="row"><span class="sw" style="background:${heat(
        0.95
      )}"></span>hotter red = more market cap</div>
        <div class="row"><span class="sw" style="background:rgba(255,255,255,0.7)"></span>blip = a company · click it</div>`;
    }
  }

  function renderFilters() {
    const el = $('#filters');
    if (!el) return;
    el.innerHTML =
      `<div class="filters-h">Industries</div>` +
      SECTORS.map((sec) => {
        const on = activeSectors.has(sec);
        return `<button class="chip ${on ? 'on' : 'off'}" data-sec="${sec}">
          <span class="cdot" style="background:${SECTOR_COLORS[sec]}"></span>${sec}</button>`;
      }).join('');
  }

  function toggleSector(sec) {
    if (activeSectors.has(sec)) activeSectors.delete(sec);
    else activeSectors.add(sec);
    rebuildAggregates();
    renderFilters();
    applyLens(currentLens);
  }

  // ---------- panel ----------
  const panel = () => $('#panel');
  function openPanel() {
    panel().classList.remove('hidden');
    world.controls().autoRotate = false;
  }
  function closePanel() {
    panel().classList.add('hidden');
  }

  function openCountry(name) {
    const c = byCountry[name];
    if (!c) return;
    openPanel();
    $('#panelBody').innerHTML = `
      <div class="p-kicker">Country lens</div>
      <div class="p-title">${name}</div>
      <div class="p-sub">${fmtCap(c.total)} in tracked market cap · ${c.companies.length} firms</div>
      <div class="section-h">Top companies here</div>
      <div class="co-list" id="coList"></div>`;
    const list = $('#coList');
    c.companies.forEach((co) => {
      const btn = document.createElement('button');
      btn.innerHTML = `<span>${co.name} <span style="color:var(--muted)">${co.ticker}</span></span><span class="cap">${fmtCap(
        co.cap
      )}</span>`;
      btn.onclick = () => openCompany(co);
      list.appendChild(btn);
    });
  }

  function openCompany(co) {
    openPanel();
    const sw = SECTOR_COLORS[co.sector] || '#fff';
    const hasSiblings = (byCountry[co.country]?.companies.length || 0) > 1;
    $('#panelBody').innerHTML = `
      ${hasSiblings ? `<button class="p-back" id="pBack">‹ other companies in ${co.country}</button>` : ''}
      <div class="p-kicker">${co.country}</div>
      <div class="p-title">${co.name}</div>
      <div class="p-sub">${co.ticker} · ${co.city} · <span style="color:${sw}">${co.sector}</span></div>
      <div class="stat-row">
        <div class="stat"><div class="label">Market cap</div><div class="val">${fmtCap(co.cap)}</div></div>
        <div class="stat"><div class="label">Price</div><div class="val" id="px">…</div></div>
        <div class="stat"><div class="label">30d</div><div class="val" id="chg">…</div></div>
      </div>
      <svg class="spark" id="spark" preserveAspectRatio="none"></svg>
      <div class="section-h">Latest news</div>
      <div class="news" id="news"><div class="loading">searching the wire…</div></div>`;
    const back = $('#pBack');
    if (back) back.onclick = () => openCountry(co.country);
    loadQuote(co.ticker);
    loadNews(co.name);
  }

  async function loadQuote(symbol) {
    try {
      const q = await fetch(`/api/quote?symbol=${encodeURIComponent(symbol)}`).then((r) => r.json());
      if (q.error || q.price == null) throw new Error();
      $('#px').textContent = `${q.price.toFixed(2)} ${q.currency}`;
      const chg = $('#chg');
      if (q.changePct != null) {
        const up = q.changePct >= 0;
        chg.textContent = `${up ? '+' : ''}${q.changePct.toFixed(2)}%`;
        chg.className = `val ${up ? 'up' : 'down'}`;
        drawSpark(q.spark, up);
      } else chg.textContent = '—';
    } catch {
      $('#px').textContent = '—';
      $('#chg').textContent = '—';
    }
  }

  function drawSpark(data, up) {
    const svg = $('#spark');
    if (!svg || !data || data.length < 2) return;
    const w = svg.clientWidth || 340;
    const h = 64;
    const min = Math.min(...data);
    const max = Math.max(...data);
    const span = max - min || 1;
    const pts = data
      .map((v, i) => `${(i / (data.length - 1)) * w},${h - ((v - min) / span) * (h - 6) - 3}`)
      .join(' ');
    const color = up ? '#6be39b' : '#ff7b7b';
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    svg.innerHTML = `<polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
  }

  async function loadNews(name) {
    const box = $('#news');
    try {
      const data = await fetch(`/api/news?q=${encodeURIComponent(name)}`).then((r) => r.json());
      const arts = (data.articles || []).slice(0, 12);
      if (!arts.length) {
        box.innerHTML = `<div class="loading">no fresh headlines found.</div>`;
        return;
      }
      box.innerHTML = arts
        .map(
          (a) => `<a href="${a.url}" target="_blank" rel="noopener">${a.title}
            <span class="meta">${a.source || ''} · ${prettyDate(a.date)}</span></a>`
        )
        .join('');
    } catch {
      box.innerHTML = `<div class="loading">couldn't reach the news wire.</div>`;
    }
  }

  function prettyDate(d) {
    if (!d) return '';
    // GDELT gives YYYYMMDDTHHMMSSZ
    const m = /^(\d{4})(\d{2})(\d{2})/.exec(d);
    if (m) return `${m[3]}/${m[2]}/${m[1]}`;
    const dt = new Date(d);
    return isNaN(dt) ? '' : dt.toLocaleDateString();
  }

  // ---------- ticker (retention hook) ----------
  async function loadTicker() {
    try {
      const data = await fetch('/api/headlines').then((r) => r.json());
      const arts = (data.articles || []).slice(0, 16);
      if (!arts.length) return;
      const track = $('#tickerTrack');
      track.innerHTML = arts
        .map(
          (a) =>
            `<a class="ticker-item" href="${a.url}" target="_blank" rel="noopener">${a.title}<span class="src">${a.source || ''}</span></a>`
        )
        .join('');
    } catch {
      $('#tickerTrack').innerHTML = `<span class="ticker-item muted">live wire offline — globe still spins.</span>`;
    }
  }

  // ---------- wire up ----------
  function bindUI() {
    document.getElementById('lenses').addEventListener('click', (e) => {
      const b = e.target.closest('.lens');
      if (b) applyLens(b.dataset.lens);
    });
    document.getElementById('filters').addEventListener('click', (e) => {
      const b = e.target.closest('.chip');
      if (b) toggleSector(b.dataset.sec);
    });
    $('#panelClose').addEventListener('click', closePanel);
    document.addEventListener('keydown', (e) => e.key === 'Escape' && closePanel());
    setTimeout(() => {
      const h = $('#hint');
      if (h) h.style.display = 'none';
    }, 9000);
  }

  // ---------- boot ----------
  (async function boot() {
    await loadData();
    initGlobe();
    renderFilters();
    bindUI();
    loadTicker();
    setInterval(loadTicker, 5 * 60 * 1000); // keep the wire fresh
  })();
})();
