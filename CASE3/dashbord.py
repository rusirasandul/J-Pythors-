import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Step 1: Load the dataset
df = pd.read_csv("C:/Users/rusir/OneDrive/Desktop/J'Pythors/CASE3/vehicles_cleaned.csv")

# Step 2: Group the data by different attributes
df_grouped_color = df.groupby('Vehicle Color').size().reset_index(name='count')
df_grouped_fuel = df.groupby('Vehicle Fuel Source').size().reset_index(name='count')
df_grouped_type = df.groupby('Vehicle Type').size().reset_index(name='count')

# Step 3: Create the plots using Plotly Express

# Color distribution bar chart
color_chart = px.bar(df_grouped_color,
                     x='Vehicle Color',
                     y='count',
                     title='Vehicle Color Distribution',
                     labels={'Vehicle Color': 'Color of Vehicle', 'count': 'Number of Vehicles'})

# Fuel type distribution bar chart
fuel_chart = px.bar(df_grouped_fuel,
                    x='Vehicle Fuel Source',
                    y='count',
                    title='Vehicle Fuel Type Distribution',
                    labels={'Vehicle Fuel Source': 'Fuel Type', 'count': 'Number of Vehicles'})

# Vehicle type distribution bar chart
vehicle_type_chart = px.bar(df_grouped_type,
                            x='Vehicle Type',
                            y='count',
                            title='Vehicle Type Distribution',
                            labels={'Vehicle Type': 'Type of Vehicle', 'count': 'Number of Vehicles'})

# Step 4: Create the layout for the dashboard
app.layout = html.Div(children=[
    html.H1("Vehicle Data Dashboard", style={'text-align': 'center'}),

    # First Chart: Vehicle Color Distribution
    html.Div(children=[
        dcc.Graph(
            id='color-chart',
            figure=color_chart
        )
    ]),

    # Second Chart: Vehicle Fuel Type Distribution
    html.Div(children=[
        dcc.Graph(
            id='fuel-chart',
            figure=fuel_chart
        )
    ]),

    # Third Chart: Vehicle Type Distribution
    html.Div(children=[
        dcc.Graph(
            id='vehicle-type-chart',
            figure=vehicle_type_chart
        )
    ]),

])

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
