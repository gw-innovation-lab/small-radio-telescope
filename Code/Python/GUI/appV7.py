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

import io
import time
import serial

ser1 = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout=1)

prevclick = 0
homeprev = 0
altforprev = 0
altrevprev = 0
azforprev = 0
azrevprev = 0
delay1 = 0
motAz = ""

# This is a list of commands in a seperate file online that my program would 
# automatically pull commands from. It will hopefully be replaced with
# one I'm having a comp sci guy produce.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# This is to shorten the command needed to reference the CSS file
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# This is where the darkness begins.   
app.layout = html.Div([
    html.Div(
            id="container",
            style={"background-color": "#4B08A1",
                  "color": "white"},
            children=[
                html.H2("Small Radio Telescope: Position Control"),
#                html.A(
#                    html.Img(src=
#                                 "https://companydirectoryprod.blob.core.windows.net/logo/0564ad80-4138-4985-a173-73628c1ed835.png"
#                        ),
#                        href="https://www.winona.edu/",
#                    )
                ],
        className="banner"
    ),
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
                        "Input Direction"
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
                            className="three columns",
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
                ),
                html.Div([
                    html.H3(
                        "SRT Direction"
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
                            id="altitude",
                            className="three columns",
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
                        html.H5(
                            "Altitude Motor"
                        )
                    ], 
                        className='Title'
                    ),
                    html.Div([
                        daq.StopButton(
                            id="alt-forward-button",
                            buttonText="Forward",
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
                            buttonText="Reverse",
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
                        html.H5(
                            "Azimuth Motor"
                        )
                    ], 
                        className='Title'
                    ),
                    html.Div([
                        daq.StopButton(
                            id="az-forward-button",
                            buttonText="Forward",
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
                            buttonText="Reverse",
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
                    dcc.Interval(
                        id='refresher',
                        interval=1000)
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
        #Must be above horizon (not sure thats what this is)
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
        deg, mins, sec = degreeSpliterRounder(az)
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
        this_str = "<0,3,9999,090>"
        #Sends string to arduino
        ser1.write(str.encode(this_str))
        homeprev = homeprev + 1

#Button to Stop motors
@app.callback(
    Output(component_id='stop-button-count', component_property='children'),
    [Input(component_id='stop-button', component_property='n_clicks')]
)

def StopButton(stop_clicks):
    this_str = "<0,0>"
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
        this_str = "<0,1,9999,0{}>".format(speed_alt)
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
        this_str = "<0,2,9999,0{}>".format(speed_alt)
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
        this_str = "<0,1,9999,0{}>".format(speed_az)
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
        this_str = "<0,2,9999,0{}>".format(speed_az)
        ser1.write(str.encode(this_str))
        azrevprev = azrevprev + 1

@app.callback(
    dash.dependencies.Output('speed-control-az', 'children'),
    [dash.dependencies.Input('az-slider', 'value')])

def AltSpeed(speed_az):
    return 'PWM Duty Cycle = "{}"'.format(speed_az)

def degreeSpliterRounder(angle):
    is_positive = angle >= 0
    angle = abs(angle)
    minutes,seconds = divmod(angle*3600,60)
    degrees,minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    deg =round(degrees)
    mins = round(minutes)
    sec = round(seconds)
    return deg, mins, sec
    
@app.callback(
    Output(component_id='altitude', component_property='children'),
    [Input(component_id='refresher', 
          component_property='n_intervals')]
)

def motorLocation(delay):
    global motAz
    ser1.write(str.encode("<9>"))
    data =ser1.readline().decode('ascii')
    data1 = data.split(" ")
    try:
        location = int(data1[0])
    except ValueError:
        return motAz
    if location <= 1003:
        azimuthDec = 90 * location / 1003
        az_deg = round(azimuthDec)
        motAz = "{}°".format(az_deg)
        data = ''
        return motAz
    if location > 1003:
        azimuthDec = 90 - 90 * (location - 1003) / 1003
        az_deg = round(azimuthDec)
        motAz = "{}°".format(az_deg)
        data = ''
        return motAz
    else:
        return motAz

if __name__ == '__main__':
    app.run_server(debug=True)
