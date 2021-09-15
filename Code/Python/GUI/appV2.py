import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output

from astropy.coordinates import EarthLocation
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import AltAz
from astropy.time import Time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

prev_clicks = 0

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                    html.H3(
                        "Object"
                    )
            ], 
                className='Title'
            ),
            html.Div([
                dcc.Input(
                    id='RA', 
                    value='24d20m30s', 
                    type='text'
                ),
                html.H5(
                    "Right Ascension", 
                    style={
                        "textAlign": "bottom"
                    }
                )
            ], 
                className='row'
            ),

            html.Div([
                dcc.Input(
                    id='DEC', 
                    value='12d24m35s', 
                    type='text'
                ),
                html.H5(
                    "Declenation", 
                    style={
                        "textAlign": "bottom"
                    }
                )
            ],
                className='row'
            ),
            html.Div([
                daq.StopButton(
                    id="go-button",
                    buttonText="Go",
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center"
                    },
                        className="three columns",
                        n_clicks=0
                )
            ],
                className="three columns"
            ),
        ],
            className="four columns"
        ),
        html.Div([
            html.Div([
                html.H3(
                    "Directions"
                )
            ], 
                className='Title'
            ),
            html.Div([
                html.Div([
                    html.Div([
                        "Altitude:  "
                    ],
                        style={
                            'textAlign': 'right'
                        },
                        className="three columns"
                    ),
                    html.Div(
                        id="alt2",
                        className="ten columns",
                        style={
                            'marginRight': '20px'
                        }
                    )
                ], 
                    className="row"
                ),
                html.Div([
                    html.Div(
                        "Azimuth:   ",
                        style={
                            'textAlign': 'right'
                        },
                        className="three columns"
                    ),
                    html.Div(
                        id="az2",
                        className="ten columns",
                        style={
                            'marginRight': '20px'
                        }
                    )
                ], 
                    className="row"
                )
            ]
            )
        ], 
            className="eight columns"
        )
    ]
    )
],
    className="row",
    style={
        'padding': '0px 10px 15px 10px',
        'marginLeft': 'auto', 
        'marginRight': 'auto', 
        "width": "900px",
        'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'
    }
)
    

@app.callback(
    Output(component_id='alt2', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)

def output_div(input_value, new_input_value, clicks):
    global prev_clicks
    if clicks > prev_clicks:
        observing_time = Time.now()
        Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
        aa = AltAz(location=Winona, obstime=observing_time)
        sky_locRAD = SkyCoord(input_value, new_input_value, frame='icrs')
        alt = sky_locRAD.transform_to(aa).alt.deg
        prev_clicks = prev_clicks + 1
        is_positive = alt >= 0
        alt = abs(alt)
        minutes,seconds = divmod(alt*3600,60)
        degrees,minutes = divmod(minutes,60)
        degrees = degrees if is_positive else -degrees
        deg =round(degrees)
        mins = round(minutes)
        sec = round(seconds)
        alt2 = "{}°{}'{}''".format(deg, mins, sec)
        return alt2
    return 
    
@app.callback(
    Output(component_id='az2', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)


def output_az(RA, DEC, clicks):
    global prev_clicks
    if clicks > prev_clicks:
        observing_time = Time.now()
        Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
        aa = AltAz(location=Winona, obstime=observing_time)
        sky_locRAD = SkyCoord(RA, DEC, frame='icrs')
        az = sky_locRAD.transform_to(aa).az.deg
        prev_clicks = prev_clicks + 1
        is_positive = az >= 0
        az = abs(az)
        minutes,seconds = divmod(az*3600,60)
        degrees,minutes = divmod(minutes,60)
        degrees = degrees if is_positive else -degrees
        deg =round(degrees)
        mins = round(minutes)
        sec = round(seconds)
        az2 = "{}°{}'{}''".format(deg, mins, sec)
        return az2
    return 


if __name__ == '__main__':
    app.run_server(debug=True)