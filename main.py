"""
Main script for generating measles data visualizations
Creates interactive HTML pages with error handling and resilience features
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from data_manager import DataManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/measles_viz.log'),
        logging.StreamHandler()
    ]
)


def create_html_wrapper(fig: go.Figure, filename: str, title: str) -> str:
    """
    Create HTML page with error handling and responsive design
    
    Args:
        fig: Plotly figure object
        filename: Output filename
        title: Page title
        
    Returns:
        HTML content as string
    """
    try:
        plot_html = fig.to_html(
            include_plotlyjs='cdn',
            div_id='chart',
            config={
                'displayModeBar': False,
                'responsive': True
            }
        )
        chart_content = plot_html
    except Exception as e:
        logging.error(f"Error converting figure to HTML for {filename}: {str(e)}")
        # Fallback error message
        chart_content = f"""
        <div style="padding: 40px; text-align: center; color: #d73027; font-family: Arial, sans-serif;">
            <h2>⚠ Visualization Temporarily Unavailable</h2>
            <p style="color: #666;">Error: {str(e)}</p>
            <p style="color: #666;">This page will update automatically during the next scheduled refresh.</p>
            <p style="color: #999; font-size: 0.9em; margin-top: 30px;">
                Last update attempt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            </p>
        </div>
        """
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }}
        #chart {{
            width: 100%;
            height: 100vh;
        }}
        .error-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
    </style>
</head>
<body>
    {chart_content}
    
    <script>
        // Notify parent window of successful load
        window.addEventListener('load', function() {{
            if (window.parent !== window) {{
                window.parent.postMessage({{
                    type: 'chartLoaded',
                    page: '{filename}'
                }}, '*');
            }}
        }});
        
        // Handle runtime errors gracefully
        window.addEventListener('error', function(e) {{
            console.error('Runtime error:', e);
            // Optionally notify parent of error
            if (window.parent !== window) {{
                window.parent.postMessage({{
                    type: 'chartError',
                    page: '{filename}',
                    error: e.message
                }}, '*');
            }}
        }});
        
        // Responsive resize handling
        window.addEventListener('resize', function() {{
            if (window.Plotly) {{
                Plotly.Plots.resize(document.getElementById('chart'));
            }}
        }});
    </script>
</body>
</html>"""
    
    return html_template


def save_html_page(html_content: str, filename: str) -> bool:
    """
    Save HTML content to file
    
    Args:
        html_content: HTML string to save
        filename: Output filename
        
    Returns:
        True if successful, False otherwise
    """
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)
    
    try:
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"✓ Created {filename}")
        return True
    except Exception as e:
        logging.error(f"✗ Failed to write {filename}: {str(e)}")
        return False


def create_timeline_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create historical measles cases timeline chart
    
    Args:
        df: DataFrame with year and cases columns
        
    Returns:
        Plotly figure or None if error
    """
    try:
        # Identify columns
        year_col = 'year' if 'year' in df.columns else df.columns[0]
        cases_col = 'cases' if 'cases' in df.columns else df.columns[1]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[year_col],
            y=df[cases_col],
            mode='lines+markers',
            name='Measles Cases',
            line=dict(color='#d73027', width=2),
            marker=dict(size=4),
            hovertemplate='<b>Year:</b> %{x}<br><b>Cases:</b> %{y:,}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': 'Historical Measles Cases in the United States',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Year',
            yaxis_title='Number of Cases',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        # Format y-axis with commas
        fig.update_yaxis(tickformat=',')
        
        return fig
    except Exception as e:
        logging.error(f"Error creating timeline chart: {str(e)}")
        return None


def create_us_measles_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create current year measles cases by state bar chart
    
    Args:
        df: DataFrame with state and cases columns
        
    Returns:
        Plotly figure or None if error
    """
    try:
        # Identify columns
        state_col = next((col for col in df.columns if 'state' in col.lower()), 'state')
        cases_col = next((col for col in df.columns if 'case' in col.lower()), 'cases')
        year_col = next((col for col in df.columns if 'year' in col.lower()), None)
        
        # Get display year for title
        display_year = datetime.now().year
        if year_col and year_col in df.columns:
            display_year = int(df[year_col].max())
        
        # Sort by cases descending
        df_sorted = df.sort_values(cases_col, ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_sorted[state_col],
            x=df_sorted[cases_col],
            orientation='h',
            marker=dict(color='#4575b4'),
            hovertemplate='<b>%{y}</b><br>Cases: %{x:,}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': f'Measles Cases by State ({display_year})',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Number of Cases',
            yaxis_title='State',
            template='plotly_white',
            height=800,
            margin=dict(l=120, r=40, t=80, b=60)
        )
        
        fig.update_xaxis(tickformat=',')
        
        return fig
    except Exception as e:
        logging.error(f"Error creating US measles chart: {str(e)}")
        return None


def create_us_map_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create geographic heatmap of measles cases
    
    Args:
        df: DataFrame with state and cases columns
        
    Returns:
        Plotly figure or None if error
    """
    try:
        # Identify columns
        state_col = next((col for col in df.columns if 'state' in col.lower()), 'state')
        cases_col = next((col for col in df.columns if 'case' in col.lower()), 'cases')
        year_col = next((col for col in df.columns if 'year' in col.lower()), None)
        
        # Get display year
        display_year = datetime.now().year
        if year_col and year_col in df.columns:
            display_year = int(df[year_col].max())
        
        fig = go.Figure(data=go.Choropleth(
            locations=df[state_col],
            z=df[cases_col],
            locationmode='USA-states',
            colorscale='Reds',
            colorbar_title="Cases",
            hovertemplate='<b>%{location}</b><br>Cases: %{z:,}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': f'Geographic Distribution of Measles Cases ({display_year})',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            template='plotly_white',
            height=600,
            margin=dict(l=0, r=0, t=80, b=0)
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating US map chart: {str(e)}")
        return None


def create_mmr_coverage_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create MMR vaccination coverage chart
    
    Args:
        df: DataFrame with state and coverage columns
        
    Returns:
        Plotly figure or None if error
    """
    try:
        # Identify columns
        state_col = next((col for col in df.columns if 'state' in col.lower()), 'state')
        coverage_col = next((col for col in df.columns if 'mmr' in col.lower() or 'coverage' in col.lower()), 'coverage')
        year_col = next((col for col in df.columns if 'year' in col.lower() or 'school_year' in col.lower()), None)
        
        # Get display year
        display_year = datetime.now().year
        if year_col and year_col in df.columns:
            if df[year_col].dtype == 'object':
                # Handle "2024-2025" format
                display_year = df[year_col].iloc[0].split('-')[0] if '-' in str(df[year_col].iloc[0]) else display_year
            else:
                display_year = int(df[year_col].max())
        
        # Sort by coverage
        df_sorted = df.sort_values(coverage_col, ascending=True)
        
        # Add color coding: red if below 95% (herd immunity threshold)
        colors = ['#d73027' if x < 95 else '#4575b4' for x in df_sorted[coverage_col]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_sorted[state_col],
            x=df_sorted[coverage_col],
            orientation='h',
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>Coverage: %{x:.1f}%<extra></extra>'
        ))
        
        # Add reference line at 95% (herd immunity threshold)
        fig.add_vline(
            x=95,
            line_dash="dash",
            line_color="green",
            annotation_text="Herd Immunity Threshold (95%)",
            annotation_position="top"
        )
        
        fig.update_layout(
            title={
                'text': f'MMR Vaccination Coverage by State ({display_year})',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Coverage (%)',
            yaxis_title='State',
            template='plotly_white',
            height=800,
            margin=dict(l=120, r=40, t=80, b=60)
        )
        
        fig.update_xaxis(range=[0, 100])
        
        return fig
    except Exception as e:
        logging.error(f"Error creating MMR coverage chart: {str(e)}")
        return None


def create_exemptions_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create vaccine exemption rates chart
    
    Args:
        df: DataFrame with state and exemption columns
        
    Returns:
        Plotly figure or None if error
    """
    try:
        # Identify columns
        state_col = next((col for col in df.columns if 'state' in col.lower()), 'state')
        exemption_col = next((col for col in df.columns if 'exempt' in col.lower()), None)
        year_col = next((col for col in df.columns if 'year' in col.lower() or 'school_year' in col.lower()), None)
        
        if exemption_col is None or exemption_col not in df.columns:
            logging.warning("No exemption column found in data")
            return None
        
        # Get display year
        display_year = datetime.now().year
        if year_col and year_col in df.columns:
            if df[year_col].dtype == 'object':
                display_year = df[year_col].iloc[0].split('-')[0] if '-' in str(df[year_col].iloc[0]) else display_year
            else:
                display_year = int(df[year_col].max())
        
        # Remove states with missing exemption data
        df_clean = df[df[exemption_col].notna()].copy()
        
        # Sort by exemption rate
        df_sorted = df_clean.sort_values(exemption_col, ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_sorted[state_col],
            x=df_sorted[exemption_col],
            orientation='h',
            marker=dict(color='#fc8d59'),
            hovertemplate='<b>%{y}</b><br>Exemption Rate: %{x:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': f'Vaccine Exemption Rates by State ({display_year})',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Exemption Rate (%)',
            yaxis_title='State',
            template='plotly_white',
            height=800,
            margin=dict(l=120, r=40, t=80, b=60)
        )
        
        return fig
    except Exception as e:
        logging.error(f"Error creating exemptions chart: {str(e)}")
        return None


def main():
    """Main application function"""
    logging.info("=" * 60)
    logging.info("Starting Measles Data Visualization Generator")
    logging.info(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logging.info("=" * 60)
    
    try:
        # Initialize data manager
        data_manager = DataManager()
        
        # Fetch all data
        logging.info("\nFetching data from sources...")
        data = data_manager.fetch_all_data()
        
        # Validate data
        validation_results = data_manager.validate_data(data)
        logging.info("\n" + "=" * 60)
        logging.info("Data Validation Results:")
        logging.info("=" * 60)
        for dataset, result in validation_results.items():
            status = "✓" if result['valid'] else "✗"
            if result['valid']:
                logging.info(f"{status} {dataset}: Valid ({result.get('rows', 0)} rows)")
            else:
                logging.warning(f"{status} {dataset}: Invalid - {result['error']}")
        
        # Check if any critical datasets failed
        critical_datasets = ['timeline', 'measles']
        failed_critical = [ds for ds in critical_datasets 
                          if not validation_results.get(ds, {}).get('valid', False)]
        
        if failed_critical:
            logging.error(f"Critical datasets failed validation: {failed_critical}")
            logging.error("Cannot proceed without critical datasets.")
            sys.exit(1)
        
        # Create output directory
        output_dir = Path('docs')
        output_dir.mkdir(exist_ok=True)
        
        # Track results
        results = {'success': [], 'failed': []}
        
        # Generate visualizations
        logging.info("\n" + "=" * 60)
        logging.info("Generating Visualizations:")
        logging.info("=" * 60)
        
        # 1. Timeline Chart
        if data['timeline'] is not None:
            fig = create_timeline_chart(data['timeline'])
            if fig:
                html = create_html_wrapper(fig, 'timeline.html', 'Measles Timeline')
                if save_html_page(html, 'timeline.html'):
                    results['success'].append('timeline.html')
                else:
                    results['failed'].append('timeline.html')
            else:
                results['failed'].append('timeline.html')
        
        # 2. US Measles Cases Chart
        if data['measles'] is not None:
            fig = create_us_measles_chart(data['measles'])
            if fig:
                html = create_html_wrapper(fig, 'us_measles.html', 'Measles Cases by State')
                if save_html_page(html, 'us_measles.html'):
                    results['success'].append('us_measles.html')
                else:
                    results['failed'].append('us_measles.html')
            else:
                results['failed'].append('us_measles.html')
        
        # 3. US Map Chart
        if data['measles'] is not None:
            fig = create_us_map_chart(data['measles'])
            if fig:
                html = create_html_wrapper(fig, 'us_map.html', 'Measles Cases Map')
                if save_html_page(html, 'us_map.html'):
                    results['success'].append('us_map.html')
                else:
                    results['failed'].append('us_map.html')
            else:
                results['failed'].append('us_map.html')
        
        # 4. MMR Coverage Chart
        if data['vaccination'] is not None:
            fig = create_mmr_coverage_chart(data['vaccination'])
            if fig:
                html = create_html_wrapper(fig, 'mmr_coverage.html', 'MMR Vaccination Coverage')
                if save_html_page(html, 'mmr_coverage.html'):
                    results['success'].append('mmr_coverage.html')
                else:
                    results['failed'].append('mmr_coverage.html')
            else:
                results['failed'].append('mmr_coverage.html')
        
        # 5. Exemptions Chart
        if data['vaccination'] is not None:
            fig = create_exemptions_chart(data['vaccination'])
            if fig:
                html = create_html_wrapper(fig, 'exemptions.html', 'Vaccine Exemptions')
                if save_html_page(html, 'exemptions.html'):
                    results['success'].append('exemptions.html')
                else:
                    results['failed'].append('exemptions.html')
            else:
                logging.warning("Exemptions chart could not be created (may be missing data)")
        
        # Summary
        logging.info("\n" + "=" * 60)
        logging.info("Generation Complete:")
        logging.info("=" * 60)
        logging.info(f"✓ Successful: {len(results['success'])} visualizations")
        if results['success']:
            for page in results['success']:
                logging.info(f"  - {page}")
        
        if results['failed']:
            logging.warning(f"✗ Failed: {len(results['failed'])} visualizations")
            for page in results['failed']:
                logging.warning(f"  - {page}")
        
        logging.info(f"\nOutput directory: {output_dir.absolute()}")
        logging.info(f"Run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        logging.info("=" * 60)
        
        # Exit with appropriate code
        if results['failed'] and not results['success']:
            sys.exit(1)  # Complete failure
        elif results['failed']:
            sys.exit(2)  # Partial failure
        else:
            sys.exit(0)  # Success
            
    except Exception as e:
        logging.error(f"Fatal error in main execution: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
