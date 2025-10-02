import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
from data_manager import DataManager
from chart_generators import *
from table_generators import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('measles_viz.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def create_html_page(fig, filename):
    """
    Create a simple HTML page with just the visualization for iframe embedding
    
    Args:
        fig: Plotly figure object
        filename (str): Output filename
    """
    # Generate the HTML with minimal styling for iframe embedding
    html_content = fig.to_html(
        include_plotlyjs='cdn',
        div_id='chart',
        config={'displayModeBar': False, 'responsive': True}
    )
    
    # Add minimal CSS for iframe compatibility
    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Measles Data Visualization</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: white;
            font-family: Arial, sans-serif;
        }}
        #chart {{
            width: 100%;
            height: 100vh;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
    
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    logging.info(f"Created {filename}")

def main():
    """Main application function"""
    logging.info("Starting Measles Data Visualization Generator")
    
    try:
        # Initialize data manager
        data_manager = DataManager()
        
        # Fetch all data
        logging.info("Fetching data from sources...")
        data = data_manager.fetch_all_data()
        
        if data is None:
            logging.error("Failed to fetch required data. Exiting.")
            sys.exit(1)
        
        # Validate data
        validation_results = data_manager.validate_data(data)
        logging.info("Data validation results:")
        for dataset, result in validation_results.items():
            if result['valid']:
                logging.info(f"  {dataset}: Valid ({result.get('rows', 0)} rows)")
            else:
                logging.warning(f"  {dataset}: Invalid - {result['error']}")
        
        # Check if any critical datasets failed validation
        critical_datasets = ['timeline', 'usmeasles', 'usmap']
        failed_critical = [ds for ds in critical_datasets 
                          if not validation_results.get(ds, {}).get('valid', False)]
        
        if failed_critical:
            logging.error(f"Critical datasets failed validation: {failed_critical}")
            sys.exit(1)
        
        # Create output directory
        output_dir = Path('docs')
        output_dir.mkdir(exist_ok=True)
        
        # Generate charts
        logging.info("Generating charts...")
        
        # NEW: Southwest Weekly Comparison Table
        try:
            weekly_fig = create_southwest_weekly_comparison(data['weekly_comparison'])
            create_html_page(weekly_fig, "southwest_weekly.html")
        except Exception as e:
            logging.error(f"Failed to create weekly comparison table: {e}")
        
        # Timeline chart
        try:
            timeline_fig = create_measles_timeline(data['timeline'])
            create_html_page(timeline_fig, "timeline.html")
        except Exception as e:
            logging.error(f"Failed to create timeline chart: {e}")
        
        # Recent trends chart
        try:
            recent_fig = create_recent_trends(data['usmeasles'], data.get('mmr', pd.DataFrame()))
            create_html_page(recent_fig, "recent_trends.html")
        except Exception as e:
            logging.error(f"Failed to create recent trends chart: {e}")
        
        # R0 comparison chart
        try:
            rnaught_fig = create_rnaught_comparison()
            create_html_page(rnaught_fig, "rnaught_comparison.html")
        except Exception as e:
            logging.error(f"Failed to create R0 comparison chart: {e}")
        
        # State map
        try:
            map_fig = create_bivariate_choropleth(data['usmap'])
            create_html_page(map_fig, "state_map.html")
        except Exception as e:
            logging.error(f"Failed to create state map: {e}")
        
        # Lives saved chart
        try:
            lives_fig = create_lives_saved_chart(data.get('vaccine_impact', pd.DataFrame()))
            create_html_page(lives_fig, "lives_saved.html")
        except Exception as e:
            logging.error(f"Failed to create lives saved chart: {e}")
        
        # Generate tables
        logging.info("Generating tables...")
        
        # Timeline table
        try:
            timeline_table = create_timeline_table(data['timeline'])
            create_html_page(timeline_table, "timeline_table.html")
        except Exception as e:
            logging.error(f"Failed to create timeline table: {e}")
        
        # Recent trends table
        try:
            recent_table = create_recent_trends_table(data['usmeasles'], data.get('mmr', pd.DataFrame()))
            create_html_page(recent_table, "recent_trends_table.html")
        except Exception as e:
            logging.error(f"Failed to create recent trends table: {e}")
        
        # R0 table
        try:
            rnaught_table = create_rnaught_table()
            create_html_page(rnaught_table, "rnaught_table.html")
        except Exception as e:
            logging.error(f"Failed to create R0 table: {e}")
        
        # State map table
        try:
            map_table = create_state_map_table(data['usmap'])
            create_html_page(map_table, "state_map_table.html")
        except Exception as e:
            logging.error(f"Failed to create state map table: {e}")
        
        # Lives saved table
        try:
            lives_table = create_lives_saved_table(data.get('vaccine_impact', pd.DataFrame()))
            create_html_page(lives_table, "lives_saved_table.html")
        except Exception as e:
            logging.error(f"Failed to create lives saved table: {e}")
        
        logging.info("Successfully generated all visualizations")
        logging.info(f"Output files created in {output_dir} directory")
        
    except Exception as e:
        logging.error(f"Critical error in main application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
