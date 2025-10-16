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
    Create a mobile-responsive HTML page for iframe embedding
    
    Args:
        fig: Plotly figure object
        filename (str): Output filename
    """
    # Configure plotly for responsive display
    config = {
        'displayModeBar': False,
        'responsive': True,
        'displaylogo': False
    }
    
    # Generate the HTML with responsive configuration
    html_content = fig.to_html(
        include_plotlyjs='cdn',
        div_id='chart',
        config=config,
        include_mathjax=False
    )
    
    # Enhanced HTML with mobile-first responsive design
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <meta name="mobile-web-app-capable" content="yes">
    <title>Measles Data Visualization</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html, body {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: white;
            font-family: Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        #chart {{
            width: 100%;
            height: 100%;
            position: relative;
        }}
        
        /* Ensure plotly responsive container works */
        .plotly-graph-div {{
            width: 100% !important;
            height: 100% !important;
        }}
        
        /* Mobile-specific optimizations */
        @media screen and (max-width: 768px) {{
            body {{
                font-size: 14px;
            }}
            
            /* Ensure touch targets are large enough */
            .plotly .modebar {{
                display: none !important;
            }}
            
            /* Prevent text selection on double-tap */
            .plotly {{
                -webkit-touch-callout: none;
                -webkit-user-select: none;
                user-select: none;
            }}
        }}
        
        /* Very small screens */
        @media screen and (max-width: 480px) {{
            body {{
                font-size: 12px;
            }}
        }}
        
        /* Loading state */
        #chart:empty::before {{
            content: "Loading...";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #666;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    {html_content}
    
    <script>
        // Ensure responsive behavior on window resize
        window.addEventListener('resize', function() {{
            var gd = document.getElementById('chart');
            if (gd && gd.layout) {{
                Plotly.Plots.resize(gd);
            }}
        }});
        
        // Handle orientation changes on mobile
        window.addEventListener('orientationchange', function() {{
            setTimeout(function() {{
                var gd = document.getElementById('chart');
                if (gd && gd.layout) {{
                    Plotly.Plots.resize(gd);
                }}
            }}, 200);
        }});
        
        // Ensure chart is properly sized on load
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                var gd = document.getElementById('chart');
                if (gd && gd.layout) {{
                    Plotly.Plots.resize(gd);
                }}
            }}, 100);
        }});
    </script>
</body>
</html>"""
    
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    logging.info(f"Created responsive {filename}")
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
    Generate all visualizations from data with per-chart fallback
    
    Args:
        data: Dictionary containing all datasets
        
    Returns:
        dict: Status of each visualization (True/False/'fallback' for success)
    """
    status = {}
    
    # Create output directory
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)
    
    def safe_generate_chart(chart_name, chart_func, *args):
        """Safely generate a chart with fallback to existing file"""
        try:
            fig = chart_func(*args)
            temp_file = output_dir / f"{chart_name}_temp.html"
            final_file = output_dir / f"{chart_name}.html"
            
            # Generate to temp location first
            create_html_page(fig, f"{chart_name}_temp.html")
            
            # Only replace existing file if generation succeeded
            temp_file.rename(final_file)
            logging.info(f"Successfully generated {chart_name}.html")
            return True
        except Exception as e:
            logging.error(f"Failed to create {chart_name}: {e}")
            # Check if old version exists
            if (output_dir / f"{chart_name}.html").exists():
                logging.warning(f"Keeping existing {chart_name}.html")
                return 'fallback'
            else:
                return False
    
    # Generate charts
    logging.info("Generating charts...")
    
    status['southwest_weekly'] = safe_generate_chart(
        'southwest_weekly', 
        create_southwest_weekly_comparison, 
        data['weekly_comparison']
    )
    
    status['timeline'] = safe_generate_chart(
        'timeline', 
        create_measles_timeline, 
        data['timeline']
    )
    
    status['recent_trends'] = safe_generate_chart(
        'recent_trends', 
        create_recent_trends, 
        data['usmeasles'], 
        data.get('mmr', pd.DataFrame())
    )
    
    status['rnaught_comparison'] = safe_generate_chart(
        'rnaught_comparison', 
        create_rnaught_comparison
    )
    
    status['state_map'] = safe_generate_chart(
        'state_map', 
        create_bivariate_choropleth, 
        data['usmap']
    )
    
    status['lives_saved'] = safe_generate_chart(
        'lives_saved', 
        create_lives_saved_chart, 
        data.get('vaccine_impact', pd.DataFrame())
    )
    
    # Generate tables
    logging.info("Generating tables...")
    
    status['timeline_table'] = safe_generate_chart(
        'timeline_table', 
        create_timeline_table, 
        data['timeline']
    )
    
    status['recent_trends_table'] = safe_generate_chart(
        'recent_trends_table', 
        create_recent_trends_table, 
        data['usmeasles'], 
        data.get('mmr', pd.DataFrame())
    )
    
    status['rnaught_table'] = safe_generate_chart(
        'rnaught_table', 
        create_rnaught_table
    )
    
    status['state_map_table'] = safe_generate_chart(
        'state_map_table', 
        create_state_map_table, 
        data['usmap']
    )
    
    status['lives_saved_table'] = safe_generate_chart(
        'lives_saved_table', 
        create_lives_saved_table, 
        data.get('vaccine_impact', pd.DataFrame())
    )
    
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
