import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from datetime import datetime

def create_measles_timeline(timeline_data):
    """
    Creates a responsive timeline chart showing measles cases over time with key vaccine milestones.
    Uses square root scaling to display both historical peaks and recent trends.

    Args:
        timeline_data: DataFrame with columns 'Year', 'Cases', optional 'Highlight'

    Returns:
        plotly Figure object
    """
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    # Enhanced color palette
    colors = {
        'primary_line': '#313695',
        'milestone_line': '#4575b4',
        'national_marker': '#74add1',
        'arizona_marker': '#fdae61',
        'annotation_bg': '#e0f3f8',
        'text_primary': 'black',
        'text_secondary': 'black',
        'text_muted': 'gray'
    }

    # Responsive font sizing system
    FONT_SIZES = {
        'title': 16,
        'axis_title': 13,
        'axis_tick': 11,
        'legend': 11,
        'annotation': 10,
        'footer': 9
    }

    FONT_FAMILY = "Arial"

    # Responsive spacing system
    SPACING = {
        'margin': {'l': 50, 'r': 30, 't': 60, 'b': 100},
        'annotation_offset': -50,
        'legend_y': 1.15,
        'footer_y': -0.22
    }

    df = timeline_data.copy()

    # Text wrapping for annotations
    def wrap_text(text, width=20):
        if pd.isna(text) or text == "":
            return None
        words = str(text).split()
        lines, line, line_len = [], [], 0
        for w in words:
            if line_len + len(w) + 1 <= width:
                line.append(w)
                line_len += len(w) + 1
            else:
                if line:
                    lines.append(" ".join(line))
                line = [w]
                line_len = len(w)
        if line:
            lines.append(" ".join(line))
        return "<br>".join(lines)

    # Prepare data
    df["Label_wrapped"] = df.get("Highlight", "").apply(wrap_text)
    has_highlights = df["Label_wrapped"].notna()
    df['Cases_sqrt'] = np.sqrt(df['Cases'])

    fig = go.Figure()

    # Main timeline - cases over time
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Cases_sqrt"],
        mode="lines",
        line=dict(color=colors['primary_line'], width=3),
        hovertemplate="<b>Year:</b> %{x}<br><b>Measles Cases:</b> %{customdata:,}<extra></extra>",
        customdata=df['Cases'],
        name="Annual Measles Cases",
        showlegend=True
    ))

    # Vaccine milestones - vertical reference lines
    # 1963 - MMR vaccine licensing
    fig.add_trace(go.Scatter(
        x=[1963, 1963],
        y=[0, df['Cases_sqrt'].max()],
        mode='lines',
        line=dict(color='black', width=2, dash="solid"),
        name="MMR Vaccine Licensed (1963)",
        showlegend=True,
        hoverinfo='skip'
    ))

    # 1989 - Two MMR doses recommendation
    fig.add_trace(go.Scatter(
        x=[1989 - 0.2, 1989 - 0.2],
        y=[0, df['Cases_sqrt'].max()],
        mode='lines',
        line=dict(color='black', width=2, dash="dash"),
        name="Two MMR Doses Recommended (1989)",
        showlegend=True,
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=[1989 + 0.2, 1989 + 0.2],
        y=[0, df['Cases_sqrt'].max()],
        mode='lines',
        line=dict(color='black', width=2, dash="dash"),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Event markers if highlights exist
    if has_highlights.any():
        highlight_data = df[has_highlights]

        # Separate Arizona events from national events
        arizona_years = [2008, 2016]
        arizona_events = highlight_data[highlight_data['Year'].isin(arizona_years)]
        national_events = highlight_data[~highlight_data['Year'].isin(arizona_years)]

        # National events - circles
        if not national_events.empty:
            fig.add_trace(go.Scatter(
                x=national_events["Year"],
                y=national_events["Cases_sqrt"],
                mode="markers",
                marker=dict(
                    size=16,
                    color=colors['national_marker'],
                    symbol="circle",
                    line=dict(color=colors['primary_line'], width=2)
                ),
                hovertemplate="<b>Year:</b> %{x}<br><b>Cases:</b> %{customdata:,}<br><b>Event:</b> %{text}<extra></extra>",
                customdata=national_events['Cases'],
                text=national_events['Label_wrapped'],
                name="National Events",
                showlegend=True
            ))

        # Arizona events - diamonds
        if not arizona_events.empty:
            fig.add_trace(go.Scatter(
                x=arizona_events["Year"],
                y=arizona_events["Cases_sqrt"],
                mode="markers",
                marker=dict(
                    size=16,
                    color=colors['arizona_marker'],
                    symbol="diamond",
                    line=dict(color=colors['primary_line'], width=2)
                ),
                hovertemplate="<b>Year:</b> %{x}<br><b>Cases:</b> %{customdata:,}<br><b>Arizona Event:</b> %{text}<extra></extra>",
                customdata=arizona_events['Cases'],
                text=arizona_events['Label_wrapped'],
                name="Arizona Events",
                showlegend=True
            ))

        # Add annotations for highlighted events
        def create_annotations(data):
            annotations = []
            for _, row in data.iterrows():
                cases = row['Cases']
                if cases >= 1_000_000:
                    cases_text = f"{cases/1_000_000:.1f}M"
                elif cases >= 1_000:
                    cases_text = f"{cases/1_000:.1f}K"
                else:
                    cases_text = f"{cases:,}"

                annotation_text = f"<b>{int(row['Year'])}</b><br>{cases_text} cases"

                if row['Year'] == 1963:
                    annotation_text += "<br><i>MMR vaccine licensed</i>"
                elif row['Year'] == 1989:
                    annotation_text += "<br><i>Two MMR doses recommended</i>"

                annotations.append(dict(
                    x=row["Year"],
                    y=row["Cases_sqrt"],
                    text=annotation_text,
                    showarrow=True,
                    arrowhead=0,
                    arrowsize=0.5,
                    arrowwidth=1.5,
                    arrowcolor='gray',
                    ax=0,
                    ay=SPACING['annotation_offset'],
                    font=dict(
                        size=FONT_SIZES['annotation'],
                        color='black',
                        family=FONT_FAMILY
                    ),
                    align="center",
                    bgcolor="rgba(255, 255, 255, 0.95)"
                ))
            return annotations

        fig.update_layout(annotations=create_annotations(highlight_data))

    # Responsive layout configuration
    last_refreshed = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    fig.update_layout(
        title=None,
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        responsive=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=SPACING['legend_y'],
            xanchor="left",
            x=0,
            font=dict(
                size=FONT_SIZES['legend'],
                color='black',
                family=FONT_FAMILY
            )
        ),
        font=dict(family=FONT_FAMILY, size=FONT_SIZES['axis_tick'], color='black'),
        margin=dict(l=SPACING['margin']['l'], r=SPACING['margin']['r'], 
                   t=SPACING['margin']['t'], b=SPACING['margin']['b'], pad=4),
        showlegend=True
    )

    # Responsive axes configuration
    fig.update_xaxes(
        title=dict(
            text="<b>Year</b>",
            font=dict(
                size=FONT_SIZES['axis_title'],
                color='black',
                family=FONT_FAMILY
            )
        ),
        tickfont=dict(
            size=FONT_SIZES['axis_tick'],
            color='black',
            family=FONT_FAMILY
        ),
        showgrid=False,
        dtick=5,
        linecolor='black',
        linewidth=2,
        automargin=True
    )

    fig.update_yaxes(
        title=dict(
            text=" ",
            font=dict(
                size=FONT_SIZES['axis_title'],
                color='black',
                family=FONT_FAMILY
            )
        ),
        showgrid=False,
        showticklabels=False,
        showline=False,
        automargin=True
    )

    # Footer note
    fig.add_annotation(
        text=(f"<b>Last refreshed:</b> {last_refreshed}<br>"
              "<i>Note: Chart uses square-root scale to show both historical peaks and recent trends</i>"),
        xref="paper", yref="paper",
        x=0.0, y=SPACING['footer_y'],
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(
            size=FONT_SIZES['footer'],
            color='gray',
            family=FONT_FAMILY
        ),
        align="left"
    )

    return fig

def create_recent_trends(usmeasles_data, mmr_data):
    """
    Creates a responsive dual-axis chart showing recent measles cases (bars) and MMR vaccination
    coverage (line) with herd immunity threshold.

    Args:
        usmeasles_data: DataFrame with columns 'year', 'cases'
        mmr_data: DataFrame with columns 'year', 'Location', 'MMR'

    Returns:
        plotly Figure object
    """
    import pandas as pd
    import plotly.graph_objects as go

    # Enhanced color palette
    colors = {
        'deep_red': '#a50026',
        'red': '#d73027',
        'orange_red': '#f46d43',
        'orange': '#fdae61',
        'light_orange': '#fee090',
        'pale_yellow': '#ffffbf',
        'pale_blue': '#e0f3f8',
        'light_blue': '#abd9e9',
        'medium_blue': '#74add1',
        'blue': '#4575b4',
        'deep_blue': '#313695'
    }

    # Responsive font sizing system
    FONT_SIZES = {
        'title': 16,
        'axis_title': 13,
        'axis_tick': 11,
        'legend': 11,
        'annotation': 10,
        'footer': 9
    }

    FONT_FAMILY = "Arial"

    # Responsive spacing system
    SPACING = {
        'margin': {'l': 50, 'r': 60, 't': 60, 'b': 100},
        'annotation_offset': -50,
        'legend_y': 1.15,
        'footer_y': -0.22
    }

    # Data validation
    if usmeasles_data.empty:
        return go.Figure()

    # Prepare measles data
    us_data = usmeasles_data.copy()
    us_data['Location'] = 'United States'
    us_data = us_data.drop_duplicates(subset=['year'])

    # Merge with vaccination data if available
    if not mmr_data.empty:
        mmr_clean = mmr_data.copy().drop_duplicates(subset=['year', 'Location'])
        us_data = pd.merge(us_data, mmr_clean, on=['year', 'Location'], how='left')

    # Filter to recent years (2015 onwards) and clean data
    us_data = us_data[us_data['year'] > 2014].copy()
    us_data = us_data.drop_duplicates(subset=['year']).sort_values('year').reset_index(drop=True)

    # Convert to numeric and remove invalid data
    numeric_cols = ['year', 'cases']
    if 'MMR' in us_data.columns:
        numeric_cols.append('MMR')

    for col in numeric_cols:
        us_data[col] = pd.to_numeric(us_data[col], errors='coerce')

    us_data = us_data.dropna(subset=['year', 'cases'])

    if us_data.empty:
        return go.Figure()

    fig = go.Figure()

    # Primary chart - measles cases as bars
    fig.add_trace(go.Bar(
        x=us_data["year"],
        y=us_data["cases"],
        name="Annual Measles Cases",
        marker=dict(color=colors['deep_blue']),
        hovertemplate="<b>Year:</b> %{x}<br><b>Cases:</b> %{y:,}<extra></extra>",
        text=us_data["cases"],
        textfont=dict(size=FONT_SIZES['annotation'], family=FONT_FAMILY, color="white"),
        textposition='auto',
        showlegend=True
    ))

    # Secondary chart - vaccination coverage line (if data exists)
    has_vaccination_data = False
    if 'MMR' in us_data.columns and not us_data['MMR'].isna().all():
        valid_vaccination = us_data.dropna(subset=['MMR'])

        if not valid_vaccination.empty:
            has_vaccination_data = True

            # Herd immunity threshold line
            fig.add_hline(
                y=95,
                line=dict(dash="dash", color="black", width=2),
                yref="y2"
            )

            # Add threshold to legend
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode="lines",
                line=dict(dash="dash", color="black", width=2),
                name="95% Herd Immunity Threshold",
                showlegend=True,
                hoverinfo='skip'
            ))

            # MMR coverage line
            fig.add_trace(go.Scatter(
                x=valid_vaccination["year"],
                y=valid_vaccination["MMR"],
                name="MMR Vaccination Coverage (%)",
                mode="lines+markers",
                line=dict(color=colors['orange'], width=3),
                marker=dict(
                    size=14,
                    color=colors['orange'],
                    line=dict(color='white', width=2)
                ),
                hovertemplate="<b>Year:</b> %{x}<br><b>Coverage:</b> %{y:.1f}%<extra></extra>",
                yaxis="y2",
                showlegend=True
            ))

    # Responsive layout configuration
    fig.update_layout(
        title=None,
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        responsive=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=SPACING['legend_y'],
            xanchor="left",
            x=0,
            font=dict(
                size=FONT_SIZES['legend'],
                color='black',
                family=FONT_FAMILY
            )
        ),
        font=dict(family=FONT_FAMILY, size=FONT_SIZES['axis_tick'], color='black'),
        margin=dict(l=SPACING['margin']['l'], 
                   r=SPACING['margin']['r'] if has_vaccination_data else 30,
                   t=SPACING['margin']['t'], 
                   b=SPACING['margin']['b'], 
                   pad=4)
    )

    # Responsive axes configuration
    # X-axis - years
    fig.update_xaxes(
        title=dict(
            text="<b>Year</b>",
            font=dict(
                size=FONT_SIZES['axis_title'],
                color='black',
                family=FONT_FAMILY
            )
        ),
        tickfont=dict(
            size=FONT_SIZES['axis_tick'],
            color='black',
            family=FONT_FAMILY
        ),
        dtick=2,
        showgrid=False,
        range=[us_data["year"].min() - 0.5, us_data["year"].max() + 0.5],
        linecolor='black',
        linewidth=2,
        automargin=True
    )

    # Primary Y-axis - measles cases
    fig.update_yaxes(
        title=dict(
            text="<b>Confirmed Measles Cases</b>",
            font=dict(
                size=FONT_SIZES['axis_title'],
                color='black',
                family=FONT_FAMILY
            )
        ),
        tickfont=dict(
            size=FONT_SIZES['axis_tick'],
            color='black',
            family=FONT_FAMILY
        ),
        showgrid=False,
        range=[0, max(us_data["cases"]) * 1.1],
        showline=False,
        automargin=True
    )

    # Secondary Y-axis - vaccination coverage (if data exists)
    if has_vaccination_data:
        fig.update_layout(
            yaxis2=dict(
                title=dict(
                    text="<b>MMR Vaccination Coverage (%)</b>",
                    font=dict(
                        size=FONT_SIZES['axis_title'],
                        color='black',
                        family=FONT_FAMILY
                    )
                ),
                tickfont=dict(
                    size=FONT_SIZES['axis_tick'],
                    color='black',
                    family=FONT_FAMILY
                ),
                overlaying="y",
                side="right",
                range=[85, 100],
                showgrid=False,
                automargin=True
            )
        )

        # Threshold annotation
        fig.add_annotation(
            x=2020.5,
            y=95,
            text="<b>95% HERD IMMUNITY THRESHOLD</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="black",
            ax=1,
            ay=-40,
            font=dict(size=FONT_SIZES['annotation'], color="white", family=FONT_FAMILY),
            align="center",
            bgcolor="black",
            borderpad=6,
            yref="y2"
        )

    # Footer note
    last_refreshed = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    fig.add_annotation(
        text=f"<b>Last refreshed:</b> {last_refreshed}",
        xref="paper", yref="paper",
        x=0.0, y=SPACING['footer_y'],
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(
            size=FONT_SIZES['footer'],
            color='gray',
            family=FONT_FAMILY
        ),
        align="left"
    )

    return fig

def create_rnaught_comparison():
    """
    Creates a responsive comparative visualization of basic reproduction numbers (R₀) across diseases.
    Shows how many people each infected person could potentially infect using a dot plot.

    Returns:
        plotly Figure object
    """
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import math

    # Enhanced color palette
    colors = {
        'deep_red': '#a50026',
        'red': '#d73027',
        'orange_red': '#f46d43',
        'orange': '#fdae61',
        'light_orange': '#fee090',
        'pale_yellow': '#ffffbf',
        'pale_blue': '#e0f3f8',
        'light_blue': '#abd9e9',
        'medium_blue': '#74add1',
        'blue': '#4575b4',
        'deep_blue': '#313695'
    }

    # Responsive font sizing system
    FONT_SIZES = {
        'title': 16,
        'axis_title': 13,
        'axis_tick': 11,
        'legend': 11,
        'annotation': 10,
        'footer': 9
    }

    FONT_FAMILY = "Arial"

    # Responsive spacing system
    SPACING = {
        'margin': {'l': 50, 'r': 30, 't': 70, 'b': 100},
        'legend_y': 1.12,
        'footer_y': -0.22
    }

    # Disease data with R₀ values
    diseases_data = {
        'Disease': ['Ebola', 'HIV', 'COVID-19 (Omicron)', 'Chickenpox', 'Mumps', 'Measles'],
        'R0': [2, 4, 9.5, 12, 14, 18]
    }
    df = pd.DataFrame(diseases_data)

    fig = go.Figure()

    # Layout parameters for dot plot
    TOTAL_DISEASES = len(df)
    X_SPACING = 5
    Y_POSITION = 0
    TOTAL_DOTS = 20
    DOT_SIZE = 14
    CIRCLE_RADIUS = 1.3
    CENTER_DOT_SIZE = 18

    # Color assignments
    INFECTED_COLOR = colors['red']
    NOT_INFECTED_COLOR = '#d3d3d3'
    INDEX_CASE_COLOR = colors['orange']

    # Generate visualization for each disease
    for i, (disease, r0) in enumerate(zip(df['Disease'], df['R0'])):
        cx = i * X_SPACING
        cy = Y_POSITION

        # Calculate positions for 20 people in circular arrangement
        angles = np.linspace(0, 2 * math.pi, TOTAL_DOTS, endpoint=False)
        x_coords = cx + CIRCLE_RADIUS * np.cos(angles)
        y_coords = cy + CIRCLE_RADIUS * np.sin(angles)

        # Add dots representing individual people
        for j in range(TOTAL_DOTS):
            if j < r0:
                dot_color = INFECTED_COLOR
                hover_text = f"{disease}: This person could be infected"
            else:
                dot_color = NOT_INFECTED_COLOR
                hover_text = f"{disease}: This person is not infected"

            fig.add_trace(go.Scatter(
                x=[x_coords[j]],
                y=[y_coords[j]],
                mode='markers',
                marker=dict(
                    size=DOT_SIZE,
                    color=dot_color,
                    line=dict(width=1.5, color='white')
                ),
                hovertemplate=f"<b>{hover_text}</b><extra></extra>",
                showlegend=False
            ))

        # Add central index case
        fig.add_trace(go.Scatter(
            x=[cx],
            y=[cy],
            mode='markers',
            marker=dict(
                size=CENTER_DOT_SIZE,
                color=INDEX_CASE_COLOR,
                line=dict(color='white', width=2)
            ),
            hovertemplate=f"<b>Original infected person</b><br><b>{disease}</b> (R₀ = {r0})<extra></extra>",
            showlegend=False
        ))

        # Add transmission lines
        line_x, line_y = [], []
        for j in range(TOTAL_DOTS):
            if j < r0:
                line_x.extend([cx, x_coords[j], None])
                line_y.extend([cy, y_coords[j], None])

        if line_x:
            fig.add_trace(go.Scatter(
                x=line_x,
                y=line_y,
                mode='lines',
                line=dict(width=1.5, color=INFECTED_COLOR),
                opacity=0.6,
                hoverinfo='skip',
                showlegend=False
            ))

        # Add disease label with R₀ value
        fig.add_annotation(
            x=cx,
            y=cy - CIRCLE_RADIUS - 1.0,
            text=f"<b>{disease}</b><br>R₀ = {r0}",
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(size=FONT_SIZES['annotation'], color="black", family=FONT_FAMILY),
            align="center"
        )

    # Calculate layout bounds
    x_min = -CIRCLE_RADIUS - 1.0
    x_max = (TOTAL_DISEASES - 1) * X_SPACING + CIRCLE_RADIUS + 1.0
    y_min = Y_POSITION - CIRCLE_RADIUS - 2.5
    y_max = Y_POSITION + CIRCLE_RADIUS + 1.0

    # Responsive layout configuration
    fig.update_layout(
        title=None,
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        responsive=True,
        font=dict(family=FONT_FAMILY, size=FONT_SIZES['axis_tick'], color='black'),
        margin=dict(l=SPACING['margin']['l'], r=SPACING['margin']['r'], 
                   t=SPACING['margin']['t'], b=SPACING['margin']['b'], pad=4),
        xaxis=dict(
            visible=False,
            range=[x_min, x_max]
        ),
        yaxis=dict(
            visible=False,
            range=[y_min, y_max],
            scaleanchor="x",
            scaleratio=1
        ),
        showlegend=False
    )

    # Add legend explanation
    fig.add_annotation(
        text='Each circle shows 20 people. The orange <span style="color:#fdae61">●</span> dot is the first infected person. Red <span style="color:#d73027">●</span> dots show potential infections (R₀). Grey <span style="color:#d3d3d3">●</span> dots are not infected people.',
        xref="paper", yref="paper",
        x=0.0, y=SPACING['legend_y'],
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(size=FONT_SIZES['legend'], color="black", family=FONT_FAMILY),
        align="left"
    )

    # Footer note
    last_refreshed = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    fig.add_annotation(
        text=(f"<b>Last refreshed:</b> {last_refreshed}<br>"),
        xref="paper", yref="paper",
        x=0.0, y=SPACING['footer_y'],
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(
            size=FONT_SIZES['footer'],
            color='gray',
            family=FONT_FAMILY
        ),
        align="left"
    )

    return fig

def create_bivariate_choropleth(usmap_data):
    """
    Creates a responsive bivariate choropleth map showing both MMR coverage and measles case rates.
    """
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    from datetime import datetime

    # 9-color bivariate palette
    bivariate_colors = [
        ['#d73027', '#f46d43', '#fdae61'],
        ['#fee090', '#ffffbf', '#e0f3f8'],
        ['#abd9e9', '#74add1', '#4575b4']
    ]

    missing_color = '#E0E0E0'

    category_labels = [
        ["High Cases, Low Vaccination", "High Cases, Medium Vaccination", "High Cases, High Vaccination"],
        ["Medium Cases, Low Vaccination", "Medium Cases, Medium Vaccination", "Medium Cases, High Vaccination"],
        ["Low Cases, Low Vaccination", "Low Cases, Medium Vaccination", "Low Cases, High Vaccination"]
    ]

    # State population lookup
    state_populations = {
        'Alabama': 5108468, 'Alaska': 733406, 'Arizona': 7431344, 'Arkansas': 3067732,
        'California': 38965193, 'Colorado': 5877610, 'Connecticut': 3617176, 'Delaware': 1031890,
        'Florida': 23244842, 'Georgia': 11029227, 'Hawaii': 1435138, 'Idaho': 1964726,
        'Illinois': 12569321, 'Indiana': 6862199, 'Iowa': 3207004, 'Kansas': 2940865,
        'Kentucky': 4555777, 'Louisiana': 4573749, 'Maine': 1395722, 'Maryland': 6164660,
        'Massachusetts': 7001399, 'Michigan': 10037261, 'Minnesota': 5757976, 'Mississippi': 2940057,
        'Missouri': 6196357, 'Montana': 1122069, 'Nebraska': 1988536, 'Nevada': 3194176,
        'New Hampshire': 1402054, 'New Jersey': 9290841, 'New Mexico': 2114371, 'New York': 19299981,
        'North Carolina': 10835491, 'North Dakota': 783926, 'Ohio': 11785935, 'Oklahoma': 4019800,
        'Oregon': 4233358, 'Pennsylvania': 12972008, 'Rhode Island': 1095962, 'South Carolina': 5373555,
        'South Dakota': 919318, 'Tennessee': 7126489, 'Texas': 30503301, 'Utah': 3417734,
        'Vermont': 647464, 'Virginia': 8715698, 'Washington': 7812880, 'West Virginia': 1770071,
        'Wisconsin': 5910955, 'Wyoming': 584057
    }

    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    state_centroids = {
        'AL': [-86.87, 32.78], 'AK': [-153.31, 64.0], 'AZ': [-111.57, 34.29], 'AR': [-92.37, 34.97],
        'CA': [-119.42, 36.78], 'CO': [-105.51, 39.06], 'CT': [-72.76, 41.60], 'DE': [-75.50, 39.00],
        'FL': [-81.69, 27.77], 'GA': [-83.64, 32.99], 'HI': [-157.86, 21.31], 'ID': [-114.58, 43.68],
        'IL': [-89.37, 40.42], 'IN': [-86.44, 40.30], 'IA': [-93.09, 41.88], 'KS': [-98.58, 38.53],
        'KY': [-84.27, 37.84], 'LA': [-91.87, 31.17], 'ME': [-69.39, 45.37], 'MD': [-76.59, 39.05],
        'MA': [-71.72, 42.34], 'MI': [-84.54, 44.18], 'MN': [-93.90, 46.39], 'MS': [-89.87, 32.74],
        'MO': [-92.28, 38.57], 'MT': [-109.45, 46.92], 'NE': [-99.90, 41.50], 'NV': [-116.94, 39.33],
        'NH': [-71.56, 43.45], 'NJ': [-74.52, 40.06], 'NM': [-106.24, 34.84], 'NY': [-75.50, 42.94],
        'NC': [-79.80, 35.63], 'ND': [-100.34, 47.53], 'OH': [-82.77, 40.42], 'OK': [-96.93, 35.56],
        'OR': [-120.57, 43.98], 'PA': [-77.20, 40.59], 'RI': [-71.51, 41.70], 'SC': [-80.95, 33.91],
        'SD': [-99.90, 44.35], 'TN': [-86.69, 35.75], 'TX': [-98.77, 31.17], 'UT': [-111.89, 40.15],
        'VT': [-72.71, 44.04], 'VA': [-78.47, 37.77], 'WA': [-121.75, 47.40], 'WV': [-80.95, 38.49],
        'WI': [-89.99, 43.78], 'WY': [-107.55, 43.08]
    }

    if usmap_data.empty:
        return go.Figure()

    df = usmap_data.copy()

    # Find cases column
    cases_col = next((c for c in ['cases_calendar_year', 'cases', 'Cases'] if c in df.columns), None)
    vaccination_col = 'Estimate (%)'

    if cases_col is None or vaccination_col not in df.columns:
        return go.Figure()

    # Prepare data
    df = df.copy()
    df['population'] = df['geography'].map(state_populations)
    df['state_code'] = df['geography'].map(state_abbrev)
    df['case_rate'] = (df[cases_col] / df['population'] * 100000).round(2).fillna(0)
    df[vaccination_col] = pd.to_numeric(df[vaccination_col], errors='coerce')

    # Identify states with missing MMR data
    missing_mmr_states_df = df[df[vaccination_col].isna()].copy()
    missing_mmr_states = missing_mmr_states_df['state_code'].tolist()

    # Remove rows with missing data for the bivariate classification
    df_clean = df.dropna(subset=[vaccination_col, 'case_rate']).copy()

    def classify_detailed_bivariate(case_rate, mmr_coverage):
        """Classify states into detailed 3x3 bivariate categories"""
        if case_rate <= 1.0:
            case_class = 2
        elif case_rate <= 3.0:
            case_class = 1
        else:
            case_class = 0

        if mmr_coverage < 92:
            mmr_class = 0
        elif mmr_coverage < 96:
            mmr_class = 1
        else:
            mmr_class = 2

        return case_class, mmr_class, category_labels[case_class][mmr_class]

    # Apply detailed bivariate classification
    classification_results = df_clean.apply(
        lambda row: classify_detailed_bivariate(row['case_rate'], row[vaccination_col]), axis=1
    )

    df_clean['case_class'] = [result[0] for result in classification_results]
    df_clean['mmr_class'] = [result[1] for result in classification_results]
    df_clean['category_label'] = [result[2] for result in classification_results]
    df_clean['color'] = [bivariate_colors[result[0]][result[1]] for result in classification_results]

    df = df.merge(df_clean[['state_code', 'color']], on='state_code', how='left')
    df['color'] = df['color'].fillna(missing_color)

    fig = go.Figure()

    # Add traces for states with missing MMR data first (grey)
    if not missing_mmr_states_df.empty:
        fig.add_trace(go.Choropleth(
            locations=missing_mmr_states_df['state_code'],
            z=[1] * len(missing_mmr_states_df),
            locationmode='USA-states',
            marker_line_color='white',
            marker_line_width=0.5,
            colorscale=[[0, missing_color], [1, missing_color]],
            showscale=False,
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Classification: Missing Data<br>'
                'Case Rate: %{customdata[1]:.1f} per 100K<br>'
                'Total Cases: %{customdata[2]}<br>'
                'Population: %{customdata[3]:,}<br>'
                '<extra></extra>'
            ),
            customdata=list(zip(
                missing_mmr_states_df['geography'],
                missing_mmr_states_df['case_rate'],
                missing_mmr_states_df[cases_col],
                missing_mmr_states_df['population']
            )),
            name="Missing Data",
            showlegend=False
        ))

    # Create separate traces for each bivariate category
    for case_class in range(3):
        for mmr_class in range(3):
            subset = df_clean[(df_clean['case_class'] == case_class) & (df_clean['mmr_class'] == mmr_class)]

            if len(subset) > 0:
                fig.add_trace(go.Choropleth(
                    locations=subset['state_code'],
                    z=[1] * len(subset),
                    locationmode='USA-states',
                    marker_line_color='white',
                    marker_line_width=0.5,
                    colorscale=[[0, bivariate_colors[case_class][mmr_class]],
                               [1, bivariate_colors[case_class][mmr_class]]],
                    showscale=False,
                    hovertemplate=(
                        '<b>%{customdata[0]}</b><br>'
                        'Classification: %{customdata[4]}<br>'
                        'MMR Coverage: %{customdata[1]:.1f}%<br>'
                        'Case Rate: %{customdata[2]:.1f} per 100K<br>'
                        'Total Cases: %{customdata[3]}<br>'
                        'Population: %{customdata[5]:,}<br>'
                        '<extra></extra>'
                    ),
                    customdata=list(zip(
                        subset['geography'],
                        subset[vaccination_col],
                        subset['case_rate'],
                        subset[cases_col],
                        subset['category_label'],
                        subset['population']
                    )),
                    showlegend=False
                ))

    # Responsive layout with full screen positioning
    fig.update_layout(
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            domain=dict(x=[0, 1.0], y=[0.0, 1.0])
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        responsive=True,
        font=dict(family='Arial, sans-serif', size=10),
        margin=dict(l=0, r=0, t=0, b=0, pad=0)
    )

    # Create 3x3 bivariate legend
    legend_x = 0.03
    legend_y = 0.95
    cell_size = 0.032
    spacing = 0.005

    # Add 3x3 legend grid
    for i in range(3):
        for j in range(3):
            fig.add_shape(
                type="rect",
                xref="paper", yref="paper",
                x0=legend_x + j * (cell_size + spacing),
                y0=legend_y - (i + 1) * (cell_size + spacing) - 0.025,
                x1=legend_x + j * (cell_size + spacing) + cell_size,
                y1=legend_y - i * (cell_size + spacing) - 0.025,
                fillcolor=bivariate_colors[i][j],
                line=dict(color="white", width=1)
            )

    # Add missing data legend square
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=legend_x,
        y0=legend_y - 4.0 * (cell_size + spacing) - 0.025,
        x1=legend_x + cell_size,
        y1=legend_y - 3.0 * (cell_size + spacing) - 0.025,
        fillcolor=missing_color,
        line=dict(color="white", width=1)
    )

    fig.add_annotation(
        text="Missing Data",
        xref="paper", yref="paper",
        x=legend_x + cell_size + spacing,
        y=legend_y - 3.5 * (cell_size + spacing) - 0.025,
        showarrow=False,
        font=dict(size=12, color='black'),
        xanchor="left", yanchor="middle"
    )

    # Add axis titles
    fig.add_annotation(
        text="← MMR Vaccine Coverage →",
        xref="paper", yref="paper",
        x=legend_x + 1.5 * (cell_size + spacing),
        y=legend_y - 0.005,
        showarrow=False,
        font=dict(size=12, color='black', family='Arial'),
        xanchor="center", 
        yanchor="bottom"
    )
    
    fig.add_annotation(
        text="← Case Rate →",
        xref="paper", yref="paper",
        x=legend_x - 0.013,
        y=legend_y - 1.5 * (cell_size + spacing) - 0.02,
        showarrow=False,
        font=dict(size=12, color='black', family='Arial'),
        xanchor="center", 
        yanchor="middle",
        textangle=90
    )

    # Function to determine text color based on background color
    def get_text_color(hex_color):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return 'black' if luminance > 0.5 else 'white'

    # Add state abbreviation labels - responsive sizing
    black_text_states = []
    white_text_states = []

    for index, row in df.iterrows():
        state_code = row.get('state_code')
        if state_code and state_code in state_centroids:
            lon, lat = state_centroids[state_code]
            background_color = row.get('color', missing_color)
            text_color = get_text_color(background_color)

            state_info = {
                'lon': lon,
                'lat': lat,
                'text': state_code,
                'state': row.get('geography', state_code)
            }

            if text_color == 'black':
                black_text_states.append(state_info)
            else:
                white_text_states.append(state_info)

    # Add black text labels
    if black_text_states:
        fig.add_trace(go.Scattergeo(
            lon=[s['lon'] for s in black_text_states],
            lat=[s['lat'] for s in black_text_states],
            text=[s['text'] for s in black_text_states],
            mode='text',
            textfont=dict(size=9, color='black', family='Arial'),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Add white text labels
    if white_text_states:
        fig.add_trace(go.Scattergeo(
            lon=[s['lon'] for s in white_text_states],
            lat=[s['lat'] for s in white_text_states],
            text=[s['text'] for s in white_text_states],
            mode='text',
            textfont=dict(size=9, color='white', family='Arial'),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Add timestamp and notes
    fig.add_annotation(
        text=(f"<b>Last refreshed:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>"
              "<i>Note: Grey states are missing vaccination coverage data from the 2024-2025 school year</i>"),
        xref="paper", yref="paper",
        x=0.02, y=0.02,
        showarrow=False,
        font=dict(size=9, color='gray'),
        xanchor="left", yanchor="bottom",
        align="left"
    )

    return fig

def create_lives_saved_chart(vaccine_impact_data):
    """
    Create responsive bar chart visualization of estimated lives saved by vaccination programs.
    """
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    from datetime import datetime
    import math

    color_palette = [
        '#d73027', '#fc8d59', '#fee090', '#ffffbf', '#e0f3f8', '#91bfdb', '#4575b4'
    ]

    if vaccine_impact_data.empty:
        return go.Figure()

    df = vaccine_impact_data.copy()

    # Flexible column name detection
    lives_saved_col = None
    for col in ['lives_saved', 'Lives_Saved', 'deaths_prevented', 'deaths_averted']:
        if col in df.columns:
            lives_saved_col = col
            break

    year_col = None
    for col in ['year', 'Year', 'calendar_year']:
        if col in df.columns:
            year_col = col
            break

    if lives_saved_col is None or year_col is None:
        return go.Figure()

    # Define custom bins
    increment = 200
    min_val = df[lives_saved_col].min()
    max_val = df[lives_saved_col].max()

    start_bin = math.floor(min_val / increment) * increment
    end_bin = math.ceil(max_val / increment) * increment + increment

    custom_bins = list(range(start_bin, end_bin, increment))

    if custom_bins[0] > min_val:
        custom_bins.insert(0, min_val)
    if custom_bins[-1] < max_val:
        custom_bins.append(max_val)

    custom_bins = sorted(list(set(custom_bins)))

    # Select colors
    num_bins = len(custom_bins) - 1
    if num_bins > len(color_palette):
        color_indices = np.linspace(0, len(color_palette) - 1, num_bins, dtype=int)
        bin_colors = [color_palette[i] for i in color_indices]
    else:
        color_indices = np.linspace(0, len(color_palette) - 1, num_bins, dtype=int)
        bin_colors = [color_palette[i] for i in color_indices]

    # Create bin labels
    bin_labels = []
    for i in range(len(custom_bins) - 1):
        lower_bound = custom_bins[i]
        upper_bound = custom_bins[i+1]
        if i == 0 and lower_bound == df[lives_saved_col].min():
            label = f"≤{upper_bound:,.0f}"
        elif i == len(custom_bins) - 2 and upper_bound == df[lives_saved_col].max():
            label = f"≥{lower_bound:,.0f}"
        else:
            label = f"{lower_bound:,.0f}-{upper_bound:,.0f}"
        bin_labels.append(label)

    # Assign each data point to a bin
    df['bin_index'] = pd.cut(df[lives_saved_col], bins=custom_bins, labels=False, include_lowest=True)
    df['color'] = df['bin_index'].map(lambda x: bin_colors[int(x)] if pd.notna(x) and int(x) < len(bin_colors) else bin_colors[0])
    df['bin_label'] = df['bin_index'].map(lambda x: bin_labels[int(x)] if pd.notna(x) and int(x) < len(bin_labels) else bin_labels[0])

    # Responsive font sizing
    FONT_SIZES = {
        'title': 16,
        'axis_title': 13,
        'axis_tick': 11,
        'legend': 11,
        'annotation': 10,
        'footer': 9
    }

    FONT_FAMILY = "Arial"

    # Responsive spacing
    SPACING = {
        'margin': {'l': 50, 'r': 30, 't': 60, 'b': 100},
        'legend_y': 1.15,
        'footer_y': -0.22
    }

    fig = go.Figure()

    # Create bars with discrete colors
    fig.add_trace(go.Bar(
        x=df[year_col],
        y=df[lives_saved_col],
        marker=dict(
            color=df['color'],
            line=dict(color='white', width=0.5)
        ),
        hovertemplate=(
            '<b>Year: %{x}</b><br>'
            'Lives Saved: %{y:,.0f}<br>'
            'Range: %{customdata}<br>'
            '<extra></extra>'
        ),
        customdata=df['bin_label'],
        showlegend=False
    ))

    # Responsive layout
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        responsive=True,
        font=dict(family=FONT_FAMILY, size=FONT_SIZES['axis_tick'], color='black'),
        margin=dict(
            l=SPACING['margin']['l'], 
            r=SPACING['margin']['r'], 
            t=SPACING['margin']['t'], 
            b=SPACING['margin']['b'],
            pad=4
        ),
        xaxis=dict(
            title='<b>Year</b>',
            showgrid=False,
            linecolor='rgba(0,0,0,0)',
            linewidth=0,
            title_font=dict(size=FONT_SIZES['axis_title'], color='black', family=FONT_FAMILY),
            tickfont=dict(size=FONT_SIZES['axis_tick'], color='black', family=FONT_FAMILY),
            automargin=True
        ),
        yaxis=dict(
            title='<b>Lives Saved (Estimated)</b>',
            showgrid=False,
            tickformat=',.0f',
            linecolor='rgba(0,0,0,0)',
            linewidth=0,
            title_font=dict(size=FONT_SIZES['axis_title'], color='black', family=FONT_FAMILY),
            tickfont=dict(size=FONT_SIZES['axis_tick'], color='black', family=FONT_FAMILY),
            automargin=True
        )
    )

    # Create horizontal legend
    legend_x = 0.0
    legend_y = SPACING['legend_y']
    cell_height = 0.03
    cell_width = 0.02
    spacing = 0.005

    legend_text = "Lives Saved Range: "
    current_x = legend_x + 0.01

    fig.add_annotation(
        text=legend_text,
        xref="paper", yref="paper",
        x=current_x, y=legend_y + cell_height/2,
        showarrow=False,
        font=dict(size=FONT_SIZES['legend'], color='black', family=FONT_FAMILY),
        xanchor="left", yanchor="middle"
    )

    estimated_title_width_paper_units = 0.13
    current_x += estimated_title_width_paper_units + 0.005

    display_bin_indices = np.linspace(0, len(bin_labels) - 1, min(len(bin_labels), 8), dtype=int)

    for i in display_bin_indices:
        fig.add_shape(
            type="rect",
            xref="paper", yref="paper",
            x0=current_x, y0=legend_y,
            x1=current_x + cell_width, y1=legend_y + cell_height,
            fillcolor=bin_colors[i],
            line=dict(color="white", width=1)
        )

        label_text = bin_labels[i]
        label_x_position = current_x + cell_width + spacing
        fig.add_annotation(
            text=label_text,
            xref="paper", yref="paper",
            x=label_x_position, y=legend_y + cell_height/2,
            showarrow=False,
            font=dict(size=FONT_SIZES['legend'], color='black', family=FONT_FAMILY),
            xanchor="left", yanchor="middle"
        )

        estimated_label_width_paper_units = len(label_text) * 0.008
        current_x = label_x_position + estimated_label_width_paper_units + spacing

    # Add footer
    last_refreshed = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    fig.add_annotation(
        text=(f"<b>Last refreshed:</b> {last_refreshed}<br>"
              "<i>Note: These are mathematical model estimates, not observed deaths</i>"),
        xref="paper", yref="paper",
        x=0.0, y=SPACING['footer_y'],
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(size=FONT_SIZES['footer'], color='gray', family=FONT_FAMILY),
        align="left"
    )

    return fig

def create_southwest_weekly_comparison(weekly_data):
    """
    Creates a responsive table showing weekly measles case comparison for Southwest states.
    """
    import plotly.graph_objects as go
    import pandas as pd
    from datetime import datetime, timedelta
    
    state_urls = {
        'Arizona': 'https://www.azdhs.gov/preparedness/epidemiology-disease-control/measles/index.php',
        'Texas': 'https://www.dshs.texas.gov/news-alerts/measles-outbreak-2025',
        'New Mexico': 'https://www.nmhealth.org/about/erd/ideb/mog/',
        'Utah': 'https://files.epi.utah.gov/Utah%20measles%20dashboard.html',
        'California': 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/measles.aspx',
        'Nevada': 'https://nvose.org/data-statistics/'
    }
    
    southwest_states = ['Arizona', 'Texas', 'New Mexico', 'Utah', 'California', 'Nevada']
    
    colors_in_order = ['rgba(208, 208, 208, 0.3)', 'rgba(215, 48, 39, 0.3)', 'rgba(252, 141, 89, 0.3)', 
                       'rgba(254, 224, 144, 0.3)', 'rgba(224, 243, 248, 0.3)', 'rgba(145, 191, 219, 0.3)', 
                       'rgba(69, 117, 180, 0.3)']
    header_color = colors_in_order[0]
    state_row_colors = colors_in_order[1:]
    
    font_colors = ['black', 'black', 'black', 'black', 'black', 'black']
    
    current_df = weekly_data.get('current', pd.DataFrame())
    previous_df = weekly_data.get('previous', pd.DataFrame())
    
    if current_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color='gray')
        )
        return fig
    
    current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    current_week_str = current_week_start.strftime('%m/%d/%y')
    
    if not previous_df.empty:
        last_week_start = current_week_start - timedelta(days=7)
        last_week_str = last_week_start.strftime('%m/%d/%y')
    else:
        last_week_str = 'N/A'
    
    current_filtered = current_df[current_df['State'].isin(southwest_states)].copy()
    
    if not previous_df.empty:
        previous_filtered = previous_df[previous_df['State'].isin(southwest_states)].copy()
        
        comparison = current_filtered[['State', 'Cases']].merge(
            previous_filtered[['State', 'Cases']],
            on='State',
            how='outer',
            suffixes=('_current', '_last')
        )
        
        comparison['Cases_current'] = comparison['Cases_current'].fillna(0).astype(int)
        comparison['Cases_last'] = comparison['Cases_last'].fillna(0).astype(int)
        comparison['Change_Value'] = comparison['Cases_current'] - comparison['Cases_last']
        
        comparison['Change_Percent'] = (
            (comparison['Change_Value'] / comparison['Cases_last'].replace(0, 1)) * 100
        ).round(1)
        
        def format_change(row):
            if row['Cases_last'] == 0 and row['Cases_current'] == 0:
                return "→ No change"
            elif row['Cases_last'] == 0 and row['Cases_current'] > 0:
                return f"↑ New ({row['Cases_current']})"
            elif row['Change_Value'] > 0:
                return f"↑ +{row['Change_Percent']:.1f}%"
            elif row['Change_Value'] < 0:
                return f"↓ {row['Change_Percent']:.1f}%"
            else:
                return "→ No change"
        
        comparison['Change'] = comparison.apply(format_change, axis=1)
        
    else:
        comparison = current_filtered[['State', 'Cases']].copy()
        comparison['Cases_current'] = comparison['Cases']
        comparison['Cases_last'] = 'N/A'
        comparison['Change'] = 'First week'
        comparison['Change_Value'] = 0
    
    for state in southwest_states:
        if state not in comparison['State'].values:
            new_row = pd.DataFrame({
                'State': [state],
                'Cases_current': [0],
                'Cases_last': [0] if not previous_df.empty else ['N/A'],
                'Change': ['No cases'],
                'Change_Value': [0]
            })
            comparison = pd.concat([comparison, new_row], ignore_index=True)
    
    # Sort by state order
    comparison['State'] = pd.Categorical(comparison['State'], categories=southwest_states, ordered=True)
    comparison = comparison.sort_values('State').reset_index(drop=True)
    
    # Prepare table data
    header_values = [
        '<b>State</b>', 
        f'<b>Current Week (Week of {current_week_str})</b>', 
        f'<b>Last Week (Week of {last_week_str})</b>', 
        '<b>Change</b>', 
        '<b>State Website</b>'
    ]
    
    # Format website links
    website_links = []
    for state in comparison['State']:
        if state in state_urls:
            website_links.append(f'<a href="{state_urls[state]}">View Dashboard ↗</a>')
        else:
            website_links.append('')
    
    cell_values = [
        comparison['State'],
        comparison['Cases_current'],
        comparison['Cases_last'],
        comparison['Change'],
        website_links
    ]
    
    # Apply colors in order to each row
    fill_colors = []
    font_color_values = []
    for col_idx in range(5):
        col_colors = []
        col_font_colors = []
        for row_idx in range(len(comparison)):
            col_colors.append(state_row_colors[row_idx])
            col_font_colors.append(font_colors[row_idx])
        fill_colors.append(col_colors)
        font_color_values.append(col_font_colors)
    
    # Create responsive Plotly table
    fig = go.Figure(data=[go.Table(
        columnwidth=[100, 100, 100, 100, 120],
        header=dict(
            values=header_values,
            fill_color=header_color,
            align=['left', 'center', 'center', 'center', 'center'],
            font=dict(color='black', size=12, family='Arial'),
            height=40
        ),
        cells=dict(
            values=cell_values,
            fill_color=fill_colors,
            align=['left', 'center', 'center', 'center', 'center'],
            font=dict(color=font_color_values, size=11, family='Arial'),
            height=35,
            line=dict(color='white', width=1)
        )
    )])
    
    # Responsive layout
    last_refreshed = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    fig.update_layout(
        title=None,
        autosize=True,
        responsive=True,
        margin=dict(l=10, r=10, t=20, b=70, pad=4),
        paper_bgcolor='white',
        font=dict(family='Arial', size=11),
        clickmode='event+select'
    )
    
    # Add footer note
    fig.add_annotation(
        text=(f"<b>Last refreshed:</b> {last_refreshed}<br>"
              "<i>Note: These numbers are according to the CDC website. For the most real-time updates, check the state's dashboards.</i>"),
        xref="paper", yref="paper",
        x=0.0, y=-0.15,
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(size=9, color='gray', family='Arial'),
        align="left"
    )
    
    return fig


# Configuration helper for displaying charts
def get_responsive_config():
    """
    Returns Plotly configuration for responsive charts.
    Use this when displaying or saving charts: fig.show(config=get_responsive_config())
    """
    return {
        'responsive': True,
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'chart',
            'height': None,
            'width': None,
            'scale': 2
        }
    }


