import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load the cleaned data using the full path
data_path = "E:/Courses/Python/project/J-Pythors-/data/vehicles_cleaned.csv"
df = pd.read_csv(data_path)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Initialize the app with a light theme
app = dash.Dash(__name__, external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css'])
app.title = "Passenger Vehicle Dashboard"

# Custom CSS for additional styling
app.layout = html.Div([
    html.Div([
        html.H1("Passenger Vehicle Dashboard", 
                style={
                    'textAlign': 'center', 
                    'color': '#333333', 
                    'fontWeight': '500', 
                    'fontSize': '32px',
                    'marginBottom': '20px'
                }
        )
    ], style={'marginBottom': '30px'}),

    # Dropdown container with improved styling
    html.Div([
        html.Label("Select Vehicle Type:", 
                   style={'color': '#555555', 'marginRight': '15px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='vehicle-type-dropdown',
            options=[{'label': vt, 'value': vt} for vt in df['vehicle type'].unique()],
            value=df['vehicle type'].unique()[0],  # Default value
            placeholder="Select Vehicle Type",
            style={
                'width': '50%', 
                'margin': '0 auto', 
                'backgroundColor': '#f5f5f5', 
                'color': '#333333',
                'border': '1px solid #ddd',
                'borderRadius': '4px',
                'padding': '8px 12px'
            },
            className='dropdown'
        )
    ], style={
        'display': 'flex', 
        'justifyContent': 'center', 
        'alignItems': 'center', 
        'marginBottom': '30px',
        'backgroundColor': '#f5f5f5',
        'padding': '15px',
        'borderRadius': '4px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),

    # Charts Container with Grid Layout
    html.Div([
        # First Row
        html.Div([
            html.Div([dcc.Graph(id='color-distribution')], className='six columns'),
            html.Div([dcc.Graph(id='fuel-source-pie-chart')], className='six columns')
        ], className='row'),

        # Second Row
        html.Div([
            html.Div([dcc.Graph(id='make-model-bar-chart')], className='six columns'),
            html.Div([dcc.Graph(id='year-trend-line-chart')], className='six columns')
        ], className='row'),

        # Third Row
        html.Div([
            html.Div([dcc.Graph(id='city-heatmap')], className='twelve columns')
        ], className='row')
    ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '4px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
], style={
    'backgroundColor': '#f5f5f5', 
    'color': '#333333', 
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px'
})

# Callback for color distribution
@app.callback(
    Output('color-distribution', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_color_distribution(selected_type):
    filtered_df = df[df['vehicle type'] == selected_type]
    fig = px.histogram(
        filtered_df, 
        x='vehicle color', 
        title=f"Color Distribution for {selected_type} Vehicles",
        labels={'vehicle color': 'Vehicle Color'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        plot_bgcolor='#fff', 
        paper_bgcolor='#fff',
        font_color='#333333',
        title_font_size=16
    )
    return fig

# Callback for fuel source pie chart
@app.callback(
    Output('fuel-source-pie-chart', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_fuel_source_pie_chart(selected_type):
    filtered_df = df[df['vehicle type'] == selected_type]
    fig = px.pie(
        filtered_df, 
        names='vehicle fuel source', 
        title=f"Fuel Source Distribution for {selected_type} Vehicles",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        plot_bgcolor='#fff', 
        paper_bgcolor='#fff',
        font_color='#333333',
        title_font_size=16
    )
    return fig

# Callback for make-model bar chart
@app.callback(
    Output('make-model-bar-chart', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_make_model_bar_chart(selected_type):
    filtered_df = df[df['vehicle type'] == selected_type]
    fig = px.bar(
        filtered_df, 
        x='vehicle make', 
        y='vehicle model year', 
        title=f"Make vs. Model Year for {selected_type} Vehicles",
        color='vehicle make',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        plot_bgcolor='#fff', 
        paper_bgcolor='#fff',
        font_color='#333333',
        title_font_size=16
    )
    return fig

# Callback for year trend line chart
@app.callback(
    Output('year-trend-line-chart', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_year_trend_line_chart(selected_type):
    filtered_df = df[df['vehicle type'] == selected_type]
    trend_df = filtered_df.groupby('vehicle model year').size().reset_index(name='count')
    fig = px.line(
        trend_df, 
        x='vehicle model year', 
        y='count', 
        title=f"Trend of {selected_type} Vehicles Over the Years",
        labels={'vehicle model year': 'Model Year', 'count': 'Count'},
        color_discrete_sequence=['#4285F4']
    )
    fig.update_layout(
        plot_bgcolor='#fff', 
        paper_bgcolor='#fff',
        font_color='#333333',
        title_font_size=16
    )
    return fig

# Callback for city heatmap
@app.callback(
    Output('city-heatmap', 'figure'),
    Input('vehicle-type-dropdown', 'value')
)
def update_city_heatmap(selected_type):
    filtered_df = df[df['vehicle type'] == selected_type]
    city_df = filtered_df.groupby('city').size().reset_index(name='count')
    fig = px.bar(
        city_df, 
        x='city', 
        y='count', 
        title=f"Vehicle Count by City for {selected_type} Vehicles",
        labels={'city': 'City', 'count': 'Vehicle Count'},
        color='count',
        color_continuous_scale=px.colors.sequential.Inferno
    )
    fig.update_layout(
        plot_bgcolor='#fff', 
        paper_bgcolor='#fff',
        font_color='#333333',
        title_font_size=16
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)