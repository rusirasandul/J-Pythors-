import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css'])
app.title = "Dashboard: Vehicles and Sentiments"

# Define some custom colors and styles
COLORS = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#e74c3c',
    'accent': '#2ecc71'
}

CONTENT_STYLE = {
    'margin-left': '2rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
    'backgroundColor': COLORS['background']
}

TAB_STYLE = {
    'padding': '12px',
    'fontWeight': 'bold',
    'backgroundColor': COLORS['background'],
    'borderBottom': f'1px solid {COLORS["primary"]}',
}

TAB_SELECTED_STYLE = {
    'padding': '12px',
    'fontWeight': 'bold',
    'backgroundColor': COLORS['primary'],
    'color': 'white',
}

# Load datasets
try:
    # Vehicle data
    vehicle_data_path = "E:/Courses/Python/project/J-Pythors-/data/vehicles_cleaned.csv"
    df_vehicle = pd.read_csv(vehicle_data_path)
    df_vehicle.columns = df_vehicle.columns.str.strip().str.lower()

    # Group data for the vehicle dashboard
    df_grouped_color = df_vehicle.groupby('vehicle color').size().reset_index(name='count')
    df_grouped_fuel = df_vehicle.groupby('vehicle fuel source').size().reset_index(name='count')

    # Shorten vehicle type labels
    vehicle_type_short_map = {
        'Charter Sightseeing': 'Charter',
        'Taxi': 'Taxi',
        'Medicar': 'Medicar',
        'Sightseeing': 'Sightseeing',
        'Ambulance': 'Ambulance',
    }
    df_vehicle['vehicle type short'] = df_vehicle['vehicle type'].map(vehicle_type_short_map).fillna(df_vehicle['vehicle type'])
    df_grouped_type_short = df_vehicle.groupby('vehicle type short').size().reset_index(name='count')

    # Sentiment data
    sentiment_data_path = "E:/Courses/Python/project/J-Pythors-/data/reviews_with_sentiments_deberta.csv"
    df_sentiment = pd.read_csv(sentiment_data_path)
    df_sentiment.columns = df_sentiment.columns.str.strip().str.lower()
except Exception as e:
    print(f"An error occurred: {e}")
    df_vehicle = pd.DataFrame()
    df_sentiment = pd.DataFrame()

# Apply common styling to charts
def apply_common_layout(fig):
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': COLORS['text']},
        title_font_size=20,
        title_x=0.5,
        margin=dict(t=40, l=40, r=40, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# Create the charts
color_chart = px.bar(
    df_grouped_color,
    x='vehicle color',
    y='count',
    title='Vehicle Color Distribution',
    color_discrete_sequence=[COLORS['primary']]
)
color_chart = apply_common_layout(color_chart)

fuel_chart = px.bar(
    df_grouped_fuel,
    x='vehicle fuel source',
    y='count',
    title='Vehicle Fuel Type Distribution',
    color_discrete_sequence=[COLORS['primary']]
)
fuel_chart = apply_common_layout(fuel_chart)

vehicle_type_chart_short = px.bar(
    df_grouped_type_short,
    x='vehicle type short',
    y='count',
    title='Vehicle Type Distribution (Shortened)',
    labels={'vehicle type short': 'Type of Vehicle', 'count': 'Number of Vehicles'},
    color_discrete_sequence=[COLORS['primary']]
)
vehicle_type_chart_short = apply_common_layout(vehicle_type_chart_short)

# Create static sentiment analysis charts
sentiment_distribution = px.pie(
    df_sentiment,
    names='sentiment',
    title="Sentiment Distribution",
    color_discrete_sequence=px.colors.qualitative.Set3
)
sentiment_distribution = apply_common_layout(sentiment_distribution)

# Fix for aspect focus chart
aspect_counts = df_sentiment['talks_about'].value_counts().reset_index()
aspect_counts.columns = ['aspect', 'count']
aspect_focus = px.bar(
    aspect_counts,
    x='aspect',
    y='count',
    title="Aspect Focus Distribution",
    labels={'aspect': 'Aspect', 'count': 'Count'},
    color_discrete_sequence=px.colors.qualitative.Set3
)
aspect_focus = apply_common_layout(aspect_focus)

sentiment_by_aspect = px.bar(
    df_sentiment.groupby(['talks_about', 'sentiment']).size().reset_index(name='count'),
    x='talks_about',
    y='count',
    color='sentiment',
    title="Sentiment by Aspect",
    labels={'talks_about': 'Aspect', 'count': 'Count'},
    color_discrete_sequence=px.colors.qualitative.Set3
)
sentiment_by_aspect = apply_common_layout(sentiment_by_aspect)

# Define the app layout
app.layout = html.Div([
    # Header
    html.H1(
        "Vehicle Analytics Dashboard",
        style={
            'textAlign': 'center',
            'color': COLORS['text'],
            'padding': '2rem',
            'backgroundColor': 'white',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginBottom': '2rem'
        }
    ),
    
    # Tabs Container
    dcc.Tabs([
        # Vehicle Data Tab
        dcc.Tab(
            label="Vehicle Data",
            style=TAB_STYLE,
            selected_style=TAB_SELECTED_STYLE,
            children=[
                html.Div([
                    # Static charts
                    html.Div([
                        dcc.Graph(figure=color_chart),
                        dcc.Graph(figure=fuel_chart),
                        dcc.Graph(figure=vehicle_type_chart_short),
                    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '2rem'})
                ], style=CONTENT_STYLE)
            ]
        ),
        
        # Sentiment Analysis Tab
        dcc.Tab(
            label="Sentiment Analysis",
            style=TAB_STYLE,
            selected_style=TAB_SELECTED_STYLE,
            children=[
                html.Div([
                    html.Div([
                        # Row 1
                        html.Div([
                            html.Div([
                                dcc.Graph(figure=sentiment_distribution)
                            ], style={'width': '48%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(figure=aspect_focus)
                            ], style={'width': '48%', 'display': 'inline-block'}),
                        ]),
                        
                        # Row 2
                        html.Div([
                            dcc.Graph(figure=sentiment_by_aspect)
                        ], style={'marginTop': '2rem'})
                    ], style={'padding': '2rem'})
                ], style=CONTENT_STYLE)
            ]
        ),
    ], style={'marginTop': '2rem'})
], style={'backgroundColor': COLORS['background']})

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

