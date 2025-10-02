# Measles Data Visualizations

Automated measles surveillance visualizations for iframe embedding. This system fetches data daily from CDC and WHO sources, generates interactive charts and tables, and deploys them to GitHub Pages.

## Overview

This repository automatically creates and updates measles-related data visualizations that can be embedded in websites, dashboards, and reports. The system runs daily, ensuring data stays current while maintaining reliability through comprehensive backup systems.

## Live Visualizations

All visualizations are available at: `https://mmcalend.github.io/ASU-HO-Measles-Visualizations/`

### Charts
- **[Timeline](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/timeline.html)** - Historical measles cases from 1912 to present with vaccine milestones
- **[Recent Trends](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/recent_trends.html)** - Recent cases (2015+) with MMR vaccination coverage
- **[R₀ Comparison](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/rnaught_comparison.html)** - Disease contagiousness comparison across diseases
- **[State Map](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/state_map.html)** - Bivariate choropleth showing case rates and vaccination coverage
- **[Lives Saved](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/lives_saved.html)** - Estimated lives saved by vaccination programs
- **[Southwest Weekly](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/southwest_weekly.html)** - Weekly case comparison for Southwest US states

### Tables
- **[Timeline Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/timeline_table.html)** - Historical data in tabular format
- **[Recent Trends Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/recent_trends_table.html)** - Recent trends data table
- **[R₀ Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/rnaught_table.html)** - Disease R₀ values in tabular format
- **[State Map Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/state_map_table.html)** - State-by-state data with classifications
- **[Lives Saved Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/lives_saved_table.html)** - Lives saved data in tabular format

### Data Sources

The system pulls data from multiple authoritative sources:

**Dynamic Data (Updated Daily at 6 am UTC):**
- CDC Measles Cases by Year: `https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesYear.json`
- CDC Measles Cases by State: `https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesMap.json`
- WHO Vaccine Impact (with vaccines): `https://github.com/WorldHealthOrganization/epi50-vaccine-impact/.../epi50_measles_vaccine.csv`
- WHO Vaccine Impact (without vaccines): `https://github.com/WorldHealthOrganization/epi50-vaccine-impact/.../epi50_measles_no_vaccine.csv`

**Static Data (Stored in Repository):**
- `data/timeline.csv` - Historical measles timeline with highlights
- `data/MMRKCoverage.csv` - Historical MMR coverage by year
- `data/MMRKCoverage25.csv` - Current school year MMR coverage by state

### Automatic Updates

**Schedule:**
- Runs daily at **6:00 AM UTC** (1:00 AM EST / 10:00 PM PST)
- Can be manually triggered via GitHub Actions
- Automatically runs on push to main branch (for testing)

**Update Process:**
1. **Data Fetching**: Downloads fresh data from CDC and WHO
2. **Backup Creation**: Saves timestamped backups of all downloaded data
3. **Data Processing**: Merges, cleans, and validates all datasets
4. **Visualization Generation**: Creates all charts and tables
5. **Deployment**: Publishes to GitHub Pages for public access

### Reliability & Fallback System

The system is designed to **never go down** even if data sources fail:

**Three-Layer Fallback:**
1. **Primary**: Fresh data from CDC/WHO APIs
2. **Secondary**: Timestamped backups in `data/backups/` (kept for 30 days, minimum 5 retained)
3. **Tertiary**: Existing visualizations in `docs/` (preserved if generation fails)
4. **Emergency**: Visualization snapshots in `data/viz_backups/` (kept for 7 days, minimum 3 retained)

**What Happens When Sources Fail:**
- If CDC/WHO APIs are down → Uses most recent backup data
- If backup data is corrupted → Keeps existing visualizations unchanged
- If generation fails entirely → Restores from visualization backup
- Workflow always succeeds → Site stays operational

## Data Structure

### Directory Layout

```
├── .github/
│   └── workflows/
│       └── update-data.yml          # GitHub Actions automation
├── data/
│   ├── backups/                     # Timestamped data backups
│   │   ├── usmeasles_20250102_060015.csv
│   │   ├── usmap_cases_20250102_060015.json
│   │   └── ...
│   ├── viz_backups/                 # Visualization snapshots
│   │   ├── docs_20250102_060015/
│   │   └── ...
│   ├── weekly_tracking/             # Weekly state case tracking
│   │   └── weekly_history.json
│   ├── timeline.csv                 # Static: Historical timeline
│   ├── MMRKCoverage.csv            # Static: Historical MMR coverage
│   └── MMRKCoverage25.csv          # Static: Current school year MMR
├── docs/                            # Generated visualizations (deployed)
│   ├── timeline.html
│   ├── recent_trends.html
│   ├── state_map.html
│   └── ...
├── chart_generators.py              # Chart creation functions
├── table_generators.py              # Table creation functions
├── chart_styles.py                  # Consistent styling/colors
├── data_manager.py                  # Data fetching and backup logic
├── main.py                          # Main orchestration script
└── requirements.txt                 # Python dependencies
```

### Data Flow

```
External APIs (CDC/WHO)
        ↓
   data_manager.py (fetch + backup)
        ↓
   Data Processing & Validation
        ↓
   chart_generators.py / table_generators.py
        ↓
   HTML Files in docs/
        ↓
   GitHub Pages Deployment
        ↓
   Public URLs for embedding
```

## Embedding Visualizations

All visualizations are designed for iframe embedding:

**Responsive Design:**
- All visualizations scale to container width
- Mobile-friendly layouts
- No external dependencies beyond Plotly CDN

### Manual Workflow Trigger

You can manually trigger the update workflow from GitHub:
1. Go to the **Actions** tab
2. Select **Update Measles Data Visualization**
3. Click **Run workflow**
4. Optionally check "Force refresh all data" to ignore caches

## Maintenance

### Backup Management

**Data Backups** (`data/backups/`):
- Automatically cleaned after 30 days
- Minimum of 5 most recent backups always retained
- Each backup is timestamped: `{source}_{YYYYMMDD_HHMMSS}.{ext}`

**Visualization Backups** (`data/viz_backups/`):
- Automatically cleaned after 7 days
- Minimum of 3 most recent backups always retained
- Each backup is a folder: `docs_{YYYYMMDD_HHMMSS}/`

### Monitoring

**Check System Health:**
1. Visit [Actions tab](https://github.com/mmcalend/ASU-HO-Measles-Visualizations/actions)
2. Look for daily workflow runs at 6 AM UTC
3. Green checkmark = successful update
4. Yellow warning = used fallback data (site still operational)
5. Red X = check logs for issues

**Key Log Messages:**
- `"Downloaded fresh data"` - Normal operation
- `"Using backup data"` - Data source temporarily unavailable
- `"Keeping existing visualizations"` - Generation failed but site preserved
- `"Restored from backup"` - Emergency fallback activated

### Troubleshooting

**If visualizations stop updating:**
1. Check if CDC/WHO APIs are accessible
2. Review the latest workflow run in Actions tab
3. Verify backups exist in `data/backups/`
4. Manually trigger workflow with "Force refresh" option

**If a data source permanently changes:**
1. Update URLs in `data_manager.py` → `self.data_sources`
2. Update processing logic in `process_data()` method if needed
3. Test locally with `python main.py`
4. Commit and push changes

## Technical Details

**Built With:**
- **Python 3.11**
- **Plotly** - Interactive visualizations
- **Pandas** - Data processing
- **GitHub Actions** - Automation
- **GitHub Pages** - Hosting

## License

This project uses public health data from CDC and WHO. Visualizations are provided for public health education and awareness.

## Contact

For questions or issues, please open an issue in this repository.

---

**Last Updated:** October 2025  
**Maintained By:** ASU Health Observatory
