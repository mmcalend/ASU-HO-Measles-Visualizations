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
    Create a MOBILE-OPTIMIZED HTML page with the visualization for iframe embedding
    FIXES: Legend/key overlap issues on mobile and small screens
    
    Args:
        fig: Plotly figure object
        filename (str): Output filename
    """
    # Apply mobile-friendly modebar settings to the figure
    fig.update_layout(
        autosize=True,
        modebar=dict(
            orientation='v',
            bgcolor='rgba(255, 255, 255, 0.9)',
            color='rgba(0, 0, 0, 0.7)',
            activecolor='rgba(0, 0, 0, 1)'
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='white',
            font_size=10,  # Smaller for mobile
            font_family='Arial'
        )
    )
    
    # Generate the HTML with mobile-optimized configuration
    html_content = fig.to_html(
        include_plotlyjs='cdn',
        div_id='chart',
        config={
            'responsive': True,
            'displayModeBar': 'hover',  # Only show on hover to save space
            'displaylogo': False,
            'modeBarButtonsToRemove': [
                'pan2d', 'lasso2d', 'select2d', 
                'zoomIn2d', 'zoomOut2d', 'autoScale2d'
            ],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': filename.replace('.html', ''),
                'height': None,
                'width': None,
                'scale': 2
            },
            'scrollZoom': False,  # Disable scroll zoom on mobile
            'doubleClick': 'reset'
        }
    )
    
    # Add responsive CSS and mobile optimizations
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=2.0, user-scalable=yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
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
            display: block;
            position: relative;
        }}
        
        /* Force Plotly components to be responsive */
        .plotly,
        .js-plotly-plot,
        .plot-container,
        .svg-container {{
            width: 100% !important;
            height: 100% !important;
        }}
        
        /* Ensure proper SVG scaling */
        .main-svg {{
            width: 100% !important;
            height: 100% !important;
        }}
        
        /* Tablet optimizations (768px and below) */
        @media (max-width: 768px) {{
            body {{
                font-size: 12px;
            }}
            
            /* Make legends more compact */
            .legend {{
                font-size: 10px !important;
                max-width: 95% !important;
            }}
            
            /* Adjust modebar for tablets */
            .modebar {{
                position: absolute !important;
                top: 5px !important;
                right: 5px !important;
                opacity: 0.8;
            }}
            
            .modebar-btn {{
                width: 28px !important;
                height: 28px !important;
            }}
            
            /* Make hover tooltips more readable */
            .hoverlayer .hovertext {{
                font-size: 11px !important;
                max-width: 250px !important;
            }}
            
            /* Reduce tick label sizes */
            .xtick text,
            .ytick text {{
                font-size: 10px !important;
            }}
            
            /* Reduce axis title sizes */
            .xtitle,
            .ytitle {{
                font-size: 11px !important;
            }}
            
            /* Make annotations more compact */
            .annotation text {{
                font-size: 9px !important;
            }}
            
            /* Fix legend spacing */
            .legend .traces {{
                display: flex !important;
                flex-wrap: wrap !important;
                gap: 8px !important;
            }}
        }}
        
        /* Mobile phone optimizations (480px and below) */
        @media (max-width: 480px) {{
            body {{
                font-size: 11px;
            }}
            
            /* Even smaller fonts */
            .legend {{
                font-size: 9px !important;
                max-width: 100% !important;
            }}
            
            .hoverlayer .hovertext {{
                font-size: 10px !important;
                max-width: 180px !important;
            }}
            
            /* Reduce tick labels further */
            .xtick text,
            .ytick text {{
                font-size: 9px !important;
            }}
            
            .xtitle,
            .ytitle {{
                font-size: 10px !important;
            }}
            
            .annotation text {{
                font-size: 8px !important;
            }}
            
            /* Smaller modebar */
            .modebar-btn {{
                width: 24px !important;
                height: 24px !important;
            }}
            
            /* Compact legend items */
            .legend .traces {{
                gap: 5px !important;
            }}
        }}
        
        /* Very small screens (320px and below) */
        @media (max-width: 320px) {{
            .legend {{
                font-size: 8px !important;
            }}
            
            .hoverlayer .hovertext {{
                font-size: 9px !important;
                max-width: 150px !important;
            }}
            
            .xtick text,
            .ytick text {{
                font-size: 8px !important;
            }}
        }}
        
        /* Prevent text selection on touch devices */
        @media (hover: none) and (pointer: coarse) {{
            * {{
                -webkit-user-select: none;
                user-select: none;
                -webkit-tap-highlight-color: transparent;
            }}
            
            /* Touch-friendly interaction areas */
            .modebar-btn,
            .legend-toggle {{
                min-width: 44px !important;
                min-height: 44px !important;
            }}
        }}
        
        /* Loading state */
        .loading {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    {html_content}
    <script>
        // Mobile-optimized resize handler with debouncing
        let resizeTimeout;
        let lastWidth = window.innerWidth;
        let lastHeight = window.innerHeight;
        
        function handleResize() {{
            clearTimeout(resizeTimeout);
            
            // Only resize if dimensions actually changed significantly (>10px)
            const currentWidth = window.innerWidth;
            const currentHeight = window.innerHeight;
            const widthDiff = Math.abs(currentWidth - lastWidth);
            const heightDiff = Math.abs(currentHeight - lastHeight);
            
            if (widthDiff > 10 || heightDiff > 10) {{
                lastWidth = currentWidth;
                lastHeight = currentHeight;
                
                resizeTimeout = setTimeout(function() {{
                    const plots = document.getElementsByClassName('js-plotly-plot');
                    for (let i = 0; i < plots.length; i++) {{
                        try {{
                            Plotly.Plots.resize(plots[i]);
                        }} catch (e) {{
                            console.warn('Resize failed:', e);
                        }}
                    }}
                }}, 250);  // 250ms debounce
            }}
        }}
        
        window.addEventListener('resize', handleResize);
        
        // Handle orientation changes on mobile (with delay for orientation to complete)
        window.addEventListener('orientationchange', function() {{
            setTimeout(handleResize, 300);
        }}); 
        
        // Initial load resize - multiple attempts for reliability
        window.addEventListener('load', function() {{
            // First attempt
            setTimeout(function() {{
                const plots = document.getElementsByClassName('js-plotly-plot');
                for (let i = 0; i < plots.length; i++) {{
                    try {{
                        Plotly.Plots.resize(plots[i]);
                    }} catch (e) {{
                        console.warn('Initial resize failed:', e);
                    }}
                }}
            }}, 100);
            
            // Second attempt (for slower devices)
            setTimeout(handleResize, 500);
        }});
        
        // Handle visibility changes (when switching tabs/apps on mobile)
        document.addEventListener('visibilitychange', function() {{
            if (!document.hidden) {{
                setTimeout(handleResize, 100);
            }}
        }});
        
        // Handle iframe resize events (when embedded in another page)
        if (window.parent !== window) {{
            // We're in an iframe
            const observer = new ResizeObserver(entries => {{
                handleResize();
            }});
            
            if (document.body) {{
                observer.observe(document.body);
            }}
        }}
        
        // Prevent zoom on double-tap (iOS)
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(event) {{
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {{
                event.preventDefault();
            }}
            lastTouchEnd = now;
        }}, false);
    </script>
</body>
</html>
"""
    
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    logging.info(f"Created mobile-optimized {filename}")

# REST OF main.py REMAINS THE SAME
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
            logging.error(f"Error details: {str(e)}", exc_info=True)
            # Check if old version exists
            if (output_dir / f"{chart_name}.html").exists():
                logging.warning(f"Keeping existing {chart_name}.html")
                return 'fallback'
            else:
                return False
    
    # Generate charts
    logging.info("Generating mobile-optimized charts...")
    
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
    logging.info("Starting Measles Data Visualization Generator (Mobile-Optimized Version)")
    
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
            logging.info("Mobile-optimized visualizations generated successfully!")
            sys.exit(0)
        
    except Exception as e:
        logging.error(f"Critical error in main application: {e}")
        logging.error(f"Full error details:", exc_info=True)
        
        # Check if we can keep existing visualizations
        if check_existing_visualizations():
            logging.warning("Critical error occurred, but existing visualizations are preserved")
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
