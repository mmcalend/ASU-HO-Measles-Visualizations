# Measles Data Visualization Dashboard

Automated data visualization system that generates interactive charts tracking measles cases and vaccination coverage across the United States. The system is designed for zero-maintenance embedding via iframes.

## Overview

This project automatically:
- Fetches measles case data and vaccination coverage from CDC APIs
- Generates interactive Plotly visualizations
- Updates data dynamically (no hardcoded years)
- Provides fallback mechanisms for API failures
- Deploys to GitHub Pages for iframe embedding

##  Generated Visualizations

The system generates five interactive HTML pages:

1. **timeline.html** - Historical measles cases timeline (1944-present)
2. **us_measles.html** - Current year measles cases by state
3. **us_map.html** - Geographic heatmap of current year cases
4. **mmr_coverage.html** - MMR vaccination coverage by state
5. **exemptions.html** - Vaccine exemption rates by state

## Data Refresh Schedule

**Current Implementation:**
- Manual refresh: Run `python main.py` locally
- Scheduled refresh: Configure via GitHub Actions (see deployment section)

**Data Sources:**
- **Measles Cases**: CDC NNDSS API (updated weekly)
- **Vaccination Coverage**: CDC SchoolVaxView API (updated annually)
- **Backup Data**: Local CSV fallbacks for all sources


### Data Flow

```
CDC APIs → DataManager → Data Validation → Chart Generation → HTML Pages → GitHub Pages
    ↓ (if API fails)
Local CSV Backups
```

### Key Features

**Dynamic Year Handling**: Automatically uses the current year's data or the most recent available year

**API Resilience**: Multi-tier fallback system:
1. Primary CDC API
2. Secondary CDC API endpoint
3. Local CSV backup

**Error Handling**: Each visualization has error boundaries that display friendly messages if rendering fails

**No External Dependencies**: Charts use CDN-hosted Plotly.js (no build step required)

## Project Structure

```
measles-viz/
├── main.py                 # Orchestration script
├── data_manager.py         # Data fetching and processing
├── backup_data/            # CSV fallback files
│   ├── measles_cases.csv
│   ├── vaccination_coverage.csv
│   └── exemptions.csv
├── docs/                   # Generated HTML files (GitHub Pages)
│   ├── timeline.html
│   ├── us_measles.html
│   ├── us_map.html
│   ├── mmr_coverage.html
│   └── exemptions.html
└── logs/                   # Application logs
    └── measles_viz.log
```

## Setup & Usage

### Prerequisites

```bash
python 3.8+
pip install pandas plotly requests
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/measles-viz.git
cd measles-viz

# Install dependencies
pip install -r requirements.txt

# Run the generator
python main.py

# View output
open docs/timeline.html
```

### Deployment to GitHub Pages

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`, folder: `/docs`

2. **Automatic Updates (Optional):**

Create `.github/workflows/update-data.yml`:

```yaml
name: Update Measles Data

on:
  schedule:
    # Run every Monday at 2 AM UTC
    - cron: '0 2 * * 1'
  workflow_dispatch:  # Allow manual triggers

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install pandas plotly requests
      
      - name: Generate visualizations
        run: python main.py
      
      - name: Commit and push if changed
        run: |
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add docs/
          git diff --quiet && git diff --staged --quiet || (git commit -m "Update visualizations [skip ci]" && git push)
```

## Configuration

### Updating Data Sources

Edit `data_manager.py`:

```python
# CDC API endpoints
TIMELINE_API = "https://data.cdc.gov/resource/your-dataset-id.json"
MEASLES_API = "https://data.cdc.gov/resource/your-dataset-id.json"
VACCINATION_API = "https://data.cdc.gov/resource/your-dataset-id.json"

# Backup data paths
BACKUP_DIR = Path('backup_data')
```

### Customizing Visualizations

Each chart function in `main.py` returns a Plotly figure:

```python
def create_timeline_chart(data):
    # Customize colors, layout, labels here
    fig = go.Figure(...)
    return fig
```

## Resilience Features

### Automatic Year Updates

The system automatically detects the current year and displays the most recent available data. No code changes needed when a new year begins.

### API Failure Handling

If CDC APIs are unavailable:
1. System logs the error
2. Attempts alternative API endpoint
3. Falls back to local CSV backup
4. Continues generating other visualizations

### Visualization Error Handling

If a chart fails to render:
- Displays user-friendly error message
- Logs detailed error information
- Other charts continue to function

## Iframe Embedding

### Basic Embed

```html
<iframe src="https://yourusername.github.io/measles-viz/timeline.html" 
        width="100%" 
        height="600" 
        frameborder="0">
</iframe>
```

### Responsive Embed

```html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
  <iframe src="https://yourusername.github.io/measles-viz/us_map.html"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
          frameborder="0">
  </iframe>
</div>
```

## Monitoring & Logs

All operations are logged to `logs/measles_viz.log`:

```
2025-10-02 14:30:00 - INFO - Starting Measles Data Visualization Generator
2025-10-02 14:30:01 - INFO - ✓ Fetched timeline data: 5,432 records
2025-10-02 14:30:02 - INFO - ✓ Fetched measles data: 2,156 records
2025-10-02 14:30:03 - INFO - ✓ Created timeline.html
...
```

Check logs regularly to ensure:
- APIs are responding
- Data validation passes
- All visualizations generate successfully

## Troubleshooting

### Issue: Blank iframe pages
**Solution:** Check browser console for JavaScript errors. Verify Plotly CDN is accessible.

### Issue: Outdated data
**Solution:** Run `python main.py` manually or check GitHub Actions workflow status.

### Issue: API timeout errors
**Solution:** System will automatically use backup CSV data. Update backup files in `backup_data/` folder.

## Maintenance Checklist

- [ ] **Monthly**: Review logs for API failures
- [ ] **Quarterly**: Update backup CSV files with latest CDC data
- [ ] **Annually**: Verify API endpoints haven't changed
- [ ] **As Needed**: Adjust chart styling/colors

