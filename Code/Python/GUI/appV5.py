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

import serial

ser1 = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout=100)

prevclick = 0
homeprev = 0
altforprev = 0
altrevprev = 0
azforprev = 0
azrevprev = 0

# This is a list of commands in a seperate file online that my program would 
# automatically pull commands from. It will hopefully be replaced with
# one I'm having a comp sci guy produce.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
                            id="alt-slider",
                            min=0,
                            max=100,
                            value=50
                        ),
                        html.Div(
                            id='speed-control-alt')
                        
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
                            id="az-slider",
                            min=0,
                            max=100,
                            value=50
                        ),
                        html.Div(
                            id='speed-control-az')
                        
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
                    html.Div(id='go-home-button-count'),
                    html.Div(id='stop-button-count'),
                    html.Div(id='alt-for-button-count'),
                    html.Div(id='alt-rev-button-count'),
                    html.Div(id='az-for-button-count'),
                    html.Div(id='az-rev-button-count'),
                ],
                    style={
                        "visibility": "hidden"
                    }
                )
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
# Connects RA and Dec coordinates to an Alt and Az output
@app.callback(
    Output(component_id='alt2', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)

def output_div(RA, DEC, clicks):
    if clicks > prevclick:
        #When are ya observing
        observing_time = Time.now()
        #where are ya observing
        Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
        #Stores loc and time
        aa = AltAz(location=Winona, obstime=observing_time)
        #Gets RA and Dec
        sky_locRAD = SkyCoord(RA, DEC, frame='icrs')
        #Splits off altitude in degrees
        alt = sky_locRAD.transform_to(aa).alt.deg
        #Must be above horizon
        is_positive = alt >= 0
        #Must be positive for rounding
        alt = abs(alt)
        #Puts into deg,min,sec
        minutes,seconds = divmod(alt*3600,60)
        degrees,minutes = divmod(minutes,60)
        #Converts back to negative if necessary
        degrees = degrees if is_positive else -degrees
        #Rounds
        deg =round(degrees)
        mins = round(minutes)
        sec = round(seconds)
        #Outputs in proper form
        alt2 = "{}°{}'{}''".format(deg, mins, sec)
        return alt2

#This is all the same as above just for Azimuth
@app.callback(
    Output(component_id='az2', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)


def output_az(RA, DEC, clicks):
    global prevclick
    if clicks > prevclick:
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
    Output(component_id='go-home-button-count', component_property='children'),
    [Input(component_id='go-home-button', component_property='n_clicks')]
)

#Go home function for telescope store position
def goHomeButton(home_clicks):
    global homeprev
    if home_clicks > homeprev:
        #String to be sent to Arduino
        this_str = "<3,9999,090>"
        #Sends string to arduino
        ser1.write(str.encode(this_str))

#Button to Stop motors
@app.callback(
    Output(component_id='stop-button-count', component_property='children'),
    [Input(component_id='stop-button', component_property='n_clicks')]
)

def StopButton(stop_clicks):
    this_str = "<0>"
    ser1.write(str.encode(this_str))

#Alt Direct Motor Control begins now
@app.callback(
    Output(component_id='alt-for-button-count', component_property='children'),
    [Input(component_id='alt-forward-button', component_property='n_clicks'),
    dash.dependencies.Input('alt-slider', 'value')]
)

def AltForButton(alt_for_clicks, speed_alt):
    global altforprev
    if alt_for_clicks > altforprev:
        this_str = "<1,9999,0{}>".format(speed_alt)
        ser1.write(str.encode(this_str))
        altforprev = altforprev + 1

@app.callback(
    Output(component_id='alt-rev-button-count', component_property='children'),
    [Input(component_id='alt-reverse-button', component_property='n_clicks'),
    dash.dependencies.Input('alt-slider', 'value')]
)

def AltForButton(alt_rev_clicks, speed_alt):
    global altrevprev
    if alt_rev_clicks > altrevprev:
        this_str = "<2,9999,0{}>".format(speed_alt)
        ser1.write(str.encode(this_str))
        altrevprev = altrevprev + 1

@app.callback(
    dash.dependencies.Output('speed-control-alt', 'children'),
    [dash.dependencies.Input('alt-slider', 'value')])

def AltSpeed(speed_alt):
    return 'PWM Duty Cycle = "{}"'.format(speed_alt)

#Azimuth Direct Motor Control Begins now
@app.callback(
    Output(component_id='az-for-button-count', component_property='children'),
    [Input(component_id='az-forward-button', component_property='n_clicks'),
    dash.dependencies.Input('az-slider', 'value')]
)

def AltForButton(az_for_clicks, speed_az):
    global azforprev
    if az_for_clicks > azforprev:
        this_str = "<1,9999,0{}>".format(speed_az)
        ser1.write(str.encode(this_str))
        azforprev = azforprev + 1

@app.callback(
    Output(component_id='az-rev-button-count', component_property='children'),
    [Input(component_id='az-reverse-button', component_property='n_clicks'),
    dash.dependencies.Input('az-slider', 'value')]
)

def AltForButton(az_rev_clicks, speed_az):
    global azrevprev
    if az_rev_clicks > azrevprev:
        this_str = "<2,9999,0{}>".format(speed_az)
        ser1.write(str.encode(this_str))
        azrevprev = azrevprev + 1

@app.callback(
    dash.dependencies.Output('speed-control-az', 'children'),
    [dash.dependencies.Input('az-slider', 'value')])

def AltSpeed(speed_az):
    return 'PWM Duty Cycle = "{}"'.format(speed_az)

if __name__ == '__main__':
    app.run_server(debug=True)