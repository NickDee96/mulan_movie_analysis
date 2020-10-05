import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd



from plots import get_pie, get_time_series

i_df = pd.read_csv("i_df.csv")
r_df = pd.read_csv("r_df.csv")
t_df = pd.read_csv("t_df.csv")
time_df = pd.read_csv("time_df.csv")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title="MULAN (2020) Seniment Analysis and topic modelling"
app.config['suppress_callback_exceptions'] = True

server = app.server
## Setting up the DashBoard layout
app.layout = dbc.Container([
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1(
                    children="MULAN (2020) Seniment Analysis and topic modelling",
                    style={
                        "text-align":"center"
                    }
                )
            ])
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3(
                children="Data Sources",
                style={
                    "text-align":"center"
                }                
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Twitter", className="card-title"),
                        html.P(
                            f"17628 Reviews"
                        ),
                    ]
                ),outline=True
            )  
        ]),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("IMDB", className="card-title"),
                        html.P(
                            f"1988 Reviews"
                        ),
                    ]
                ),outline=True
            )  
        ]),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Rotten Tomatoes", className="card-title"),
                        html.P(
                            f"282 Reviews"
                        ),
                    ]
                ),outline=True
            )  
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(
                children="Sentiment Analysis Proportions within the various data sources",
                style={
                    "text-align":"center"
                }                
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Twitter", className="card-title"),
                        dcc.Graph(figure = get_pie(t_df),config={'displayModeBar': False})
                    ]
                ),outline=True
            ) 
        ]),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("IMDB", className="card-title"),
                        dcc.Graph(figure = get_pie(i_df),config={'displayModeBar': False})
                    ]
                ),outline=True
            ) 
        ]),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Rotten Tomatoes", className="card-title"),
                        dcc.Graph(figure = get_pie(r_df),config={'displayModeBar': False})
                    ]
                ),outline=True
            ) 
        ]),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3(
                children="Time series of sentiment within the past month",
                style={
                    "text-align":"center"
                }                
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure = get_time_series(time_df)
            )
        ])
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3(
                children="Topic modelling for positive sentiment",
                style={
                    "text-align":"center"
                }                
            )
        ])
    ]),    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Iframe(
                    src=app.get_asset_url("positive_lda.html"),
                    style=dict( left="0", top="0", width="100%", height="1000px")
                )
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(
                children="Topic modelling for negative sentiment",
                style={
                    "text-align":"center"
                }                
            )
        ])
    ]),    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Iframe(
                    src=app.get_asset_url("negative_lda.html"),
                    style=dict( left="0", top="0", width="100%", height="1000px")
                )
            ])
        ])
    ]),
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0",port=8050,debug=True)