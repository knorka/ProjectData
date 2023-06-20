
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Předpokládáme, že df je váš DataFrame
df = pd.read_excel("Ideologie.xlsx")


# Převedení sloupce 'market_indices' na číselný formát
df['market_indices'] = pd.to_numeric(df['market_indices'], errors='coerce')

# Nahrazení NaN hodnot nulou
df['market_indices'] = df['market_indices'].fillna(0)

# Seznam všech zemí pro výběr v dropdown
countries = df['country_name'].unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in countries],
        value='Germany'  # Výchozí hodnota
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    [Input(component_id='country-dropdown', component_property='value')]
)
def update_graph(selected_dropdown_value):
    dff = df[df['country_name'] == selected_dropdown_value]
    dff['rounded_market_indices'] = round(dff['market_indices'], 1)
    return {
        'data': [
            go.Scatter(
                x=dff['year'],
                y=dff['market_indices'],
                mode='lines+markers',
                hoverinfo='text',
                hovertext=dff['year'].astype(str) + ', ' + dff['rounded_market_indices'].astype(str)
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Rok'},
            yaxis={'title': '% změna hodnoty akciového indexu'},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)