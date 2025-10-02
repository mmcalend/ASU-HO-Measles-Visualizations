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

def check_existing_visualizations():
    """
    Check if visualization files already exist in docs directory
    
    Returns:
        bool: True if all critical files exist, False otherwise
    """
    output_dir = Path('docs')
    critical_files = [
        'timeline.html',
        'recent_trends.html',
        'rnaught_comparison.html',
        'state_map.html',
        'lives_saved.html'
    ]
    
    if not output_dir.exists():
        return False
    
    existing_files = [f for f in critical_files if (output_dir / f).exists()]
    
    if len(existing_files) == len(critical_files):
        logging.info(f"All {len(critical_files)} critical visualization files exist")
        return True
    else:
        logging.info(f"Only {len(existing_files)}/{len(critical_files)} critical files exist")
        return False

def generate_visualizations(data):
    """
    Generate all visualizations from data
    
    Args:
        data: Dictionary containing all datasets
        
    Returns:
        dict: Status of each visualization (True/False for success)
    """
    status = {}
    
    # Create output directory
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)
    
    # Generate charts
    logging.info("Generating charts...")
    
    # Southwest Weekly Comparison Table
    try:
        weekly_fig = create_southwest_weekly_comparison(data['weekly_comparison'])
        create_html_page(weekly_fig, "southwest_weekly.html")
        status['southwest_weekly'] = True
    except Exception as e:
        logging.error(f"Failed to create weekly comparison table: {e}")
        status['southwest_weekly'] = False
    
    # Timeline chart
    try:
        timeline_fig = create_measles_timeline(data['timeline'])
        create_html_page(timeline_fig, "timeline.html")
        status['timeline'] = True
    except Exception as e:
        logging.error(f"Failed to create timeline chart: {e}")
        status['timeline'] = False
    
    # Recent trends chart
    try:
        recent_fig = create_recent_trends(data['usmeasles'], data.get('mmr', pd.DataFrame()))
        create_html_page(recent_fig, "recent_trends.html")
        status['recent_trends'] = True
    except Exception as e:
        logging.error(f"Failed to create recent trends chart: {e}")
        status['recent_trends'] = False
    
    # R0 comparison chart
    try:
        rnaught_fig = create_rnaught_comparison()
        create_html_page(rnaught_fig, "rnaught_comparison.html")
        status['rnaught_comparison'] = True
    except Exception as e:
        logging.error(f"Failed to create R0 comparison chart: {e}")
        status['rnaught_comparison'] = False
    
    # State map
    try:
        map_fig = create_bivariate_choropleth(data['usmap'])
        create_html_page(map_fig, "state_map.html")
        status['state_map'] = True
    except Exception as e:
        logging.error(f"Failed to create state map: {e}")
        status['state_map'] = False
    
    # Lives saved chart
    try:
        lives_fig = create_lives_saved_chart(data.get('vaccine_impact', pd.DataFrame()))
        create_html_page(lives_fig, "lives_saved.html")
        status['lives_saved'] = True
    except Exception as e:
        logging.error(f"Failed to create lives saved chart: {e}")
        status['lives_saved'] = False
    
    # Generate tables
    logging.info("Generating tables...")
    
    # Timeline table
    try:
        timeline_table = create_timeline_table(data['timeline'])
        create_html_page(timeline_table, "timeline_table.html")
        status['timeline_table'] = True
    except Exception as e:
        logging.error(f"Failed to create timeline table: {e}")
        status['timeline_table'] = False
    
    # Recent trends table
    try:
        recent_table = create_recent_trends_table(data['usmeasles'], data.get('mmr', pd.DataFrame()))
        create_html_page(recent_table, "recent_trends_table.html")
        status['recent_trends_table'] = True
    except Exception as e:
        logging.error(f"Failed to create recent trends table: {e}")
        status['recent_trends_table'] = False
    
    # R0 table
    try:
        rnaught_table = create_rnaught_table()
        create_html_page(rnaught_table, "rnaught_table.html")
        status['rnaught_table'] = True
    except Exception as e:
        logging.error(f"Failed to create R0 table: {e}")
        status['rnaught_table'] = False
    
    # State map table
    try:
        map_table = create_state_map_table(data['usmap'])
        create_html_page(map_table, "state_map_table.html")
        status['state_map_table'] = True
    except Exception as e:
        logging.error(f"Failed to create state map table: {e}")
        status['state_map_table'] = False
    
    # Lives saved table
    try:
        lives_table = create_lives_saved_table(data.get('vaccine_impact', pd.DataFrame()))
        create_html_page(lives_table, "lives_saved_table.html")
        status['lives_saved_table'] = True
    except Exception as e:
        logging.error(f"Failed to create lives saved table: {e}")
        status['lives_saved_table'] = False
    
    return status

def main():
    """Main application function with improved fallback handling"""
    logging.info("Starting Measles Data Visualization Generator")
    
    try:
        # Check if existing visualizations are present
        has_existing_viz = check_existing_visualizations()
        
        # Initialize data manager
        data_manager = DataManager()
        
        # Fetch all data
        logging.info("Fetching data from sources...")
        data = data_manager.fetch_all_data()
        
        if data is None:
            logging.error("Failed to fetch required data.")
            
            if has_existing_viz:
                logging.warning("Keeping existing visualizations - no updates applied")
                logging.info("Existing visualizations are still available")
                sys.exit(0)  # Exit successfully to prevent workflow failure
            else:
                logging.error("No existing visualizations found. Cannot proceed.")
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
            
            if has_existing_viz:
                logging.warning("Keeping existing visualizations due to validation failures")
                logging.info("Existing visualizations are still available")
                sys.exit(0)  # Exit successfully to prevent workflow failure
            else:
                logging.error("No existing visualizations to fall back on.")
                sys.exit(1)
        
        # Generate all visualizations
        status = generate_visualizations(data)
        
        # Log results
        successful = sum(1 for v in status.values() if v)
        total = len(status)
        
        logging.info(f"Successfully generated {successful}/{total} visualizations")
        
        if successful > 0:
            logging.info(f"Output files created in docs directory")
            
            # List what succeeded and what failed
            logging.info("Success status:")
            for viz_name, success in status.items():
                status_str = "✓" if success else "✗"
                logging.info(f"  {status_str} {viz_name}")
        
        # Exit with success if at least some visualizations were created
        if successful == 0 and not has_existing_viz:
            logging.error("No visualizations were generated and no existing ones found")
            sys.exit(1)
        else:
            sys.exit(0)
        
    except Exception as e:
        logging.error(f"Critical error in main application: {e}")
        
        # Check if we can keep existing visualizations
        if check_existing_visualizations():
            logging.warning("Critical error occurred, but existing visualizations are preserved")
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
