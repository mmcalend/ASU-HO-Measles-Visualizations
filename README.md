# Measles Data Visualizations

Automated measles surveillance visualizations for iframe embedding.

## What This Is

This repository generates individual HTML pages for each chart and table, designed to be embedded as iframes in other websites.

## Individual Pages Generated

**Charts:**
- `timeline.html` - Historical measles timeline
- `recent_trends.html` - Recent cases and vaccination trends  
- `rnaught_comparison.html` - Disease contagiousness comparison
- `state_map.html` - State-by-state map
- `lives_saved.html` - Lives saved by vaccination

**Tables:**
- `timeline_table.html` - Historical data table
- `recent_trends_table.html` - Recent trends data table
- `rnaught_table.html` - Disease R0 values table
- `state_map_table.html` - State data table
- `lives_saved_table.html` - Lives saved data table

## Live Links


- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/timeline.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/recent_trends.html  
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/rnaught_comparison.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/state_map.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/lives_saved.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/timeline_table.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/recent_trends_table.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/rnaught_table.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/state_map_table.html
- https://mmcalend.github.io/ASU-HO-Measles-Visualizations/lives_saved_table.html

## Automatic Updates

- Runs daily at 6 AM UTC
- Fetches fresh data from CDC and WHO
- Falls back to cached data if sources are down
- All pages update automatically

## Setup

1. Enable GitHub Pages: Settings → Pages → Source: "GitHub Actions"
2. Add data files to `data/` directory
3. Workflow runs automatically

## Data Sources

- CDC Measles Cases (live data)
- WHO Vaccine Impact Database (live data)  
- State vaccination coverage files (repository data)

---

*Each visualization updates automatically with the latest public health data.*

