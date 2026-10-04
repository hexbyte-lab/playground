# 🌍 WealthGlobe

A tactile, black-and-white 3D globe that **lights up with the world's corporate wealth**.
Spin it, pick a lens, and watch market caps glow. Click a hotspot to drill into a
company's live news and stock chart — or a country to see its biggest firms.

## The design

- **Core function:** a monochrome `globe.gl` (Three.js) globe — drag, zoom, auto-spin.
- **Core loop:** spin → switch lens → read the heat → click a hotspot → live news +
  stock → drill back out → repeat.
- **Lenses (one surface):**
  - **Companies** — every major public company as a glowing spike; taller/brighter = bigger market cap.
  - **Countries** — choropleth of corporate wealth aggregated by HQ.
  - **Sectors** — points recolored by industry.
- **Retention hook:** a live business-headlines "wire" along the bottom, refreshed
  every 5 minutes, plus live per-company news and 30-day stock sparklines.

## Data sources (all key-free)

- **News:** [GDELT](https://www.gdeltproject.org/) global news API, with a Hacker News fallback.
- **Stocks:** Yahoo Finance chart endpoint (price, % change, sparkline).
- **Borders:** Natural Earth 110m GeoJSON (cached to disk after first fetch).
- **Market caps:** a curated dataset of ~75 of the world's largest public companies
  (`public/data/companies.json`).

A small Node/Express server proxies these so the browser never hits CORS or needs a key.

## Run it

```bash
cd wealth-globe
npm install
npm start
```

Then open **http://localhost:3000**.

> Requires Node 18+ (uses the built-in `fetch`). Needs internet for live news/stocks;
> the globe itself still works offline once borders are cached.
