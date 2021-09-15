import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State

from astropy.coordinates import EarthLocation
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import AltAz
from astropy.time import Time

# This is a list of commands in a seperate file online that my program would 
# automatically pull commands from. It will hopefully be replaced with
# one I'm having a comp sci guy produce.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Temporary (I think) variables to store previous button states.


# This is to shorten the command needed to reference the CSS file
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# This is where the darkness begins.   
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
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
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
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
                    className='row'
                ),
                html.Div([
                    daq.StopButton(
                        id="go-button",
                        buttonText="Go",
                        style={
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "flex-end"
                        },
                            className="three columns",
                            n_clicks=0
                    )
                ],                
                    style={
                        "align-items": "center",
                        
                        "padding": "10px 10px 10px 20px"
                    },
                    className="twelve columns"
                )
            ],
                style={
                        "align-items": "center",
                        'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
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
                            className="four columns",
                            style={
                                'marginRight': '20px'
                            }
                        )
                    ], 
                        className="twelve columns"
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
                            className="four columns",
                            style={
                                'marginRight': '20px'
                            }
                        )
                    ], 
                        className="twelve columns"
                    )
                ],
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
                    className="twelve columns"
                )
            ],
                style={
                    "align-items": "center",
                    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                    "padding": "10px 10px 10px 20px"
                },
                className="four columns"
            ),
            html.Div([
                html.Div([
                    html.H3(
                        "Direct Control"
                    )
                ], 
                    className='Title'
                ),
                html.Div([
                     daq.StopButton(
                            id="stop-button",
                            buttonText="STOP",
                            style={
                                "display": "flex",
                                "justify-content": "space-around",
                                "padding": "10px 10px 10px 10px"
                            },
                            className="six columns",
                            n_clicks=0
                        ),
                    daq.StopButton(
                            id="go-home-button",
                            buttonText="Go Home",
                            style={
                                "display": "flex-right",
                                "justify-content": "space-around",
                                "padding": "10px 10px 10px 10px"
                            },
                            className="six columns",
                            n_clicks=0
                        )
                ],
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
                    className="row"
                ),
html.Div([
                    html.Div([
                        daq.StopButton(
                            id="az-forward-button",
                            buttonText="Az Forward",
                            style={
                                "display": "flex",
                                "justify-content": "space-around",
                                "align-items": "center",
                                "padding": "10px 10px 10px 10px"
                            },
                            className="six columns",
                            n_clicks=0
                        ),
                        daq.StopButton(
                            id="az-reverse-button",
                            buttonText="Az Reverse",
                            style={
                                "display": "flex",
                                "justify-content": "space-around",
                                "align-items": "flex-end",
                                "padding": "10px 10px 10px 10px"
                            },
                            className="six columns",
                            n_clicks=0
                        )
                    ],
                        className="row"
                    ),
                    html.Div([
                        dcc.Slider(
                            id="my-slider",
                            min=0,
                            max=100,
                            value=50
                        ),
                        html.Div(
                            id='slider-output-container')
                        
                    ],
                        style={
                        "padding": "10px 10px 10px 20px"
                    },
                        className="row"
                    )
                ],
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
                        className="row"
                ),
                html.Div([
                    html.Div([
                        daq.StopButton(
                            id="alt-forward-button",
                            buttonText="Alt Forward",
                            style={
                                "display": "flex",
                                "justify-content": "space-around",
                                "align-items": "center",
                                "padding": "10px 10px 10px 10px"
                            },
                            className="six columns",
                            n_clicks=0
                        ),
                        daq.StopButton(
                            id="alt-reverse-button",
                            buttonText="Alt Reverse",
                            style={
                                "display": "flex",
                                "justify-content": "space-around",
                                "align-items": "flex-end",
                                "padding": "10px 10px 10px 10px"
                            },
                            className="six columns",
                            n_clicks=0
                        )
                    ],
                        className="row"
                    ),
                    html.Div([
                        dcc.Slider(
                            id="my-slider2",
                            min=0,
                            max=100,
                            value=50
                        ),
                        html.Div(
                            id='slider-output-container2')
                        
                    ],
                        style={
                        "padding": "10px 10px 10px 20px"
                    },
                        className="row"
                    )
                ],
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
                        className="row"
                ),
        ],
                style={
                    "align-items": "center",
                    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                    "padding": "10px 10px 10px 20px"
                },
            className="four columns"
        )
    ],
        className="row"
    )
    ],
        style={
            'padding': '0px 10px 15px 10px',
            'marginLeft': 'auto', 
            'marginRight': 'auto',
            "width": "900px",
            'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'
        }

)

# We're back in the land of the living.

@app.callback(
    Output(component_id='alt2', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)

def output_div(RA, DEC, clicks):
    observing_time = Time.now()
    Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
    aa = AltAz(location=Winona, obstime=observing_time)
    sky_locRAD = SkyCoord(RA, DEC, frame='icrs')
    alt = sky_locRAD.transform_to(aa).alt.deg
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
    
@app.callback(
    Output(component_id='az2', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)


def output_az(RA, DEC, clicks):
    observing_time = Time.now()
    Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
    aa = AltAz(location=Winona, obstime=observing_time)
    sky_locRAD = SkyCoord(RA, DEC, frame='icrs')
    az = sky_locRAD.transform_to(aa).az.deg
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

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return 'PWM Duty Cycle = "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-container2', 'children'),
    [dash.dependencies.Input('my-slider2', 'value')])
def update_output(value):
    return 'PWM Duty Cycle = "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)