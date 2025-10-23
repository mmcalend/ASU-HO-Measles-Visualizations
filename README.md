# Measles Data Visualizations

Automated measles surveillance visualizations for iframe embedding. This system fetches data daily from CDC and WHO sources, generates interactive charts and tables, and deploys them to GitHub Pages.

## Overview

This repository automatically creates and updates measles-related data visualizations that can be embedded in websites, dashboards, and reports. The system runs daily, ensuring data stays current while maintaining reliability through comprehensive backup systems.

## Live Visualizations

All visualizations are available at: `https://mmcalend.github.io/ASU-HO-Measles-Visualizations/`

### Visualization Catalog

| Title | Time Period | Visual Description | Data Sources | Chart Link | Table Link |
|-------|-------------|-------------------|--------------|------------|------------|
| **Timeline of Measles in the United States** | Confirmed measles cases and historical highlights (1960-2025) | Line chart showing United States measles cases from 1960 to 2025 on a square root scale. The line shows high numbers starting in 1960 followed by a dramatic decline after the 1963 MMR vaccine introduction (marked with a solid vertical line). Cases dropped to very low levels, with the 1989 two-dose recommendation (marked with dashed vertical lines) further reducing outbreaks. Notable events are marked with colored dots, including Arizona-specific outbreaks in 2008 and 2016. | Historical Data (1960-2024): Public Health Reports; US Census Bureau; CDC - processed by Our World in Data<br>Current Data (2025): [CDC Measles Surveillance](https://www.cdc.gov/measles/data-research/index.html)<br>Historical References:<br>(1) [History of Vaccines](https://historyofvaccines.org/history/measles/timeline)<br>(2) [CDC History](https://www.cdc.gov/measles/about/history.html)<br>(3) [Journal of Infectious Diseases](https://academic.oup.com/jid/article/203/11/1517/862546)<br>(4) [MMWR Weekly - 2017](https://www.cdc.gov/mmwr/volumes/66/wr/mm6620a5.htm)<br>(5) [MMWR Weekly - 2019](https://www.cdc.gov/mmwr/volumes/68/wr/mm6840e2.htm) | [View Chart](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/timeline.html) | [View Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/timeline_table.html) |
| **Measles Cases and Vaccination Coverage in the United States** | 2015-2025 | Dual-axis bar and line chart showing U.S. measles cases from 2015-2025 as blue bars with white text labels, and MMR vaccination coverage as an orange line with circular markers. A horizontal black dashed line marks the 95% herd immunity threshold. The bars show varying outbreak sizes with 2025 having the highest peak and lowest vaccination coverage. | MMR Vaccination Coverage (CDC NIS): [CDC Vaccination Coverage Data](https://data.cdc.gov/Vaccinations/Vaccination-Coverage-and-Exemptions-among-Kinderga/ijqb-a7ye/about_data)<br>Measles Cases & Herd Immunity Reference: [CDC Surveillance](https://www.cdc.gov/measles/data-research/index.html) | [View Chart](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/recent_trends.html) | [View Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/recent_trends_table.html) |
| **How Contagious are Different Diseases Compared to Measles?** | Visual comparison showing how many people one infected person could potentially infect | Dot plot comparing disease transmission rates across six diseases, each shown as a circle of 20 dots representing people. From left to right: Ebola shows 1 orange central dot (infected person) connected to 2 red dots (potential infections) with 18 gray dots (uninfected); HIV shows 1 orange dot connected to 4 red dots with 16 gray dots; COVID-19 Omicron shows 1 orange dot connected to 9-10 red dots with remaining gray dots; Chickenpox shows 1 orange dot connected to 12 red dots with 8 gray dots; Mumps shows 1 orange dot connected to 14 red dots with 6 gray dots; Measles shows 1 orange dot connected to 18 red dots with 2 gray dots. Red lines connect the central orange dot to each red dot showing transmission pathways. Disease names and R₀ values are labeled below each circle. | Ebola, Measles: [University of Michigan School of Public Health](https://sph.umich.edu/pursuit/2020posts/how-scientists-quantify-outbreaks.html)<br>COVID-19 Omicron Variant: [Liu and Rocklöv, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8992231)<br>Chickenpox, Mumps: [Journal of Theoretical Biology](https://www.sciencedirect.com/science/article/abs/pii/S0022519399910640?via%3Dihub)<br>HIV: [Proceedings of the National Academy of Sciences](https://www.pnas.org/content/pnas/111/45/16202.full.pdf) | [View Chart](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/rnaught_comparison.html) | [View Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/rnaught_table.html) |
| **2025 Measles Cases and Vaccination Rates by State** | Bivariate analysis combining MMR vaccination rates and measles incidence across U.S. states | Bivariate choropleth map of the United States showing measles vaccination coverage and case rates combined into a single color scheme. Each state is colored according to a 3×3 classification system: states range from red (high case rates, low vaccination) through yellow and orange (mixed risk levels) to blue (low case rates, high vaccination). State abbreviations are overlaid on each state in contrasting colors for readability. A 3×3 colored legend grid appears in the upper left corner with arrows indicating 'MMR Vaccine Coverage' horizontally and 'Case Rate' vertically. Gray states indicate missing vaccination data. | MMR Vaccination Coverage (CDC NIS): [CDC Vaccination Coverage Data](https://data.cdc.gov/Vaccinations/Vaccination-Coverage-and-Exemptions-among-Kinderga/ijqb-a7ye/about_data)<br>Measles Cases: [CDC Surveillance](https://www.cdc.gov/measles/data-research/index.html) | [View Chart](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/state_map.html) | [View Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/state_map_table.html) |
| **Estimating: How Many Lives do Vaccines Save Each Year?** | United States: Simulated estimates using WHO EPI50 mathematical models (not real observed data) | Vertical bar chart showing mathematical model estimated lives saved by measles vaccination programs over multiple years. Bars are colored according to ranges of lives saved, progressing from darker blue (lower ranges) to lighter colors and orange-red (higher ranges). Each bar shows the number of lives saved for that year, with values ranging from hundreds to potentially thousands. A horizontal legend at the top displays colored squares with corresponding numerical ranges. The x-axis shows years, and the y-axis shows estimated lives saved. | WHO EPI50 Mathematical Models; 2024 United States: [Full Data Published in the Lancet](https://github.com/WorldHealthOrganization/epi50-vaccine-impact) | [View Chart](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/lives_saved.html) | [View Table](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/lives_saved_table.html) |
| **Measles Cases in the Southwestern United States** | Week-over-week comparison | Table showing current and previous week's measles case counts for six southwestern states (Arizona, Texas, New Mexico, Utah, California, Nevada). Each row represents a state with colored backgrounds, displaying current week cases, last week cases, change indicators (arrows and percentages), and links to state health department dashboards. | Current Week Data: [CDC Measles Cases Map](https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesMap.json)<br>Historical Tracking: Weekly snapshots stored in repository<br>State Dashboards: Individual state health department websites | [View Chart](https://mmcalend.github.io/ASU-HO-Measles-Visualizations/southwest_weekly.html) |[CDC Measles Surveillance](https://www.cdc.gov/measles/data-research/index.html) |

### How Data is Processed

**Timeline Chart:**
- Combines historical data from Our World in Data (1960-2024) with current CDC surveillance data (2025)
- Applies square root transformation to Y-axis to visualize both historical peaks and recent trends
- Merges timeline highlights (vaccine milestones, notable outbreaks) with case counts by year

**Recent Trends Chart:**
- Merges CDC annual case counts (2015-2025) with NIS kindergarten MMR coverage data
- Filters to recent years (>2014) and removes duplicates
- Calculates dual-axis scaling to show both case counts and vaccination percentages

**R₀ Comparison Chart:**
- Uses hardcoded R₀ values from peer-reviewed literature
- Generates circular dot arrangements using trigonometric positioning
- No external data fetching required (static visualization)

**State Map:**
- Merges CDC state-level case data with NIS state-level MMR coverage data
- Calculates case rates per 100,000 population using 2020 Census data
- Applies bivariate classification (3×3 grid) based on case rate and vaccination thresholds
- Assigns colors from red (high risk) to blue (low risk) based on classification

**Lives Saved Chart:**
- Fetches WHO EPI50 mathematical model data for USA from GitHub
- Merges "with vaccine" and "without vaccine" mortality estimates by year
- Calculates lives saved as difference between no-vaccine and with-vaccine scenarios
- Creates discrete color bins based on lives saved ranges

**Southwest Weekly Table:**
- Extracts fresh state-level case data from CDC API on each run
- Saves current week's data as JSON snapshot in `data/weekly_tracking/`
- Loads previous week's snapshot from history file for comparison
- Calculates week-over-week changes (absolute and percentage)
- Maintains 8 weeks of rolling history

### Data Sources

The system pulls data from multiple authoritative sources:

**Dynamic Data (Updated Daily at 6 AM UTC):**
- CDC Measles Cases by Year: `https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesYear.json`
- CDC Measles Cases by State: `https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesMap.json`
- WHO Vaccine Impact (with vaccines): `https://github.com/WorldHealthOrganization/epi50-vaccine-impact/.../epi50_measles_vaccine.csv`
- WHO Vaccine Impact (without vaccines): `https://github.com/WorldHealthOrganization/epi50-vaccine-impact/.../epi50_measles_no_vaccine.csv`

**Static Data (Stored in Repository):**
- `data/timeline.csv` - Historical measles timeline with highlights
- `data/MMRKCoverage.csv` - Historical MMR coverage by year
- `data/MMRKCoverage25.csv` - Current school year MMR coverage by state
- `data/weekly_tracking/weekly_history.json` - Weekly state case snapshots (rolling 8 weeks)

### Automatic Updates

**Schedule:**
- Runs daily at **6:00 AM UTC** (1:00 AM EST / 10:00 PM PST)
- Can be manually triggered via GitHub Actions
- Automatically runs on push to main branch (for testing)

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
