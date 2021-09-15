import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        daq.StopButton(
            id="stop-button",
            buttonText="Stop",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
            className="three columns",
            n_clicks=0,
            )
    ],
        className="four columns"
    ),
    html.Div([
        daq.StopButton(
            id="forward-button",
            buttonText="Forward",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
            className="three columns",
            n_clicks=0,
            )
    ],
        className="four columns"
    ),
    html.Div([
        daq.StopButton(
            id="reverse-button",
            buttonText="Reverse",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
            className="three columns",
            n_clicks=0,
            )
        ],
        className="four columns"
    )
    

],
    style={
                "border-radius": "10px",
                "border-width": "30px",
                "border": "1px solid rgb(216, 216, 216)",
                "height": "90%",
                "width": "90%"
            }

)

if __name__ == '__main__':
    app.run_server(debug=True)