import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State

from astropy.coordinates import EarthLocation
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import AltAz
from astropy.coordinates import get_body
from astropy.time import Time
from astropy.table import Table

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

from IPython.display import Image
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)


import time
import serial

#Initialize serial communication, this is often commented out to see the webpage when the Arduino is not hooked up
#ser1 = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout=1)

#Dummy variables for keeping track of button presses.
prevclick = 0
homeprev = 0
altforprev = 0
altrevprev = 0
azforprev = 0
azrevprev = 0
delay1 = 0
#Blank string to be updated for updating the realtime location of the gear/dish
motAz = ""

# This is a list of commands in a seperate file online that my program would 
# automatically pull commands from. It will hopefully be replaced with
# one I'm having a comp sci guy produce.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# This is to shorten the command needed to reference the CSS file as well as the Dash libraries
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# This is where the darkness begins.   
app.layout = html.Div([
    #Start with the banner at the top of the page
    html.Div(
            id="container",
            style={"background-color": "#4B08A1",
                  "color": "white"},
            children=[
                    html.H3("Small Radio Telescope Control"),
                #Something goes wrong here, Im trying to put the Winona State symbol in that links to the WSU homepage. It works, its just not in the upper right 
#                    html.A(
#                        html.Img(src=
#                                 "https://mfr.osf.io/export?url=https://osf.io/xa6p8/?action=download%26mode=render%26direct%26public_file=False&initialWidth=675&childId=mfrIframe&parentTitle=OSF+%7C+NewWinona22.PNG&parentUrl=https://osf.io/xa6p8/&format=2400x2400.jpeg"                            ),
#                    href="https://www.winona.edu/",
#                        )
            ],
        className="banner"
    ),
    #Setup for the graph to display objects seen from Earth
    html.Div([
        #Dropdown bar to choose which planet will be selected
        html.Div([
            dcc.Dropdown(
                #ID for callback function
                id='solarsystem',
                #Dropdown selection options
                options=[
                    {'label': 'Object', 'value': 'object'},
                    {'label': 'Sun', 'value': 'sun'},
                    {'label': 'Moon', 'value': 'moon'},
                    {'label': 'Mercury', 'value': 'mercury'},
                    {'label': 'Venus', 'value': 'venus'},
                    {'label': 'Mars', 'value': 'mars'},
                    {'label': 'Jupiter', 'value': 'jupiter'},
                    {'label': 'Saturn', 'value': 'saturn'},
                    {'label': 'Uranus', 'value': 'uranus'},
                    {'label': 'Neptune', 'value': 'neptune'},
                ],
                #initial value
                value='sun'
            )
        ]
        ),
        #Initialize graph and id for callback
        html.Div([
            dcc.Graph(
                id='graph'
            )
        ],
            className="twelve columns",
            style={
                "marginTop": "5%"
            }
        )
    ],
        #Take up the full width of the page
        className='twelve columns'
    ),
    #Seperate the rest of the page
    html.Div([
        #Direct control compartment of the page
        html.Div([
                html.Div([
                    #Title
                    html.H3(
                        "Direct Control"
                    )
                ], 
                    className='Title'
                ),
            #Two buttons per row
                html.Div([
                     daq.StopButton(
                            id="stop-button",
                            buttonText="STOP",
                            style={
                                #Not entirely sure how these work, padding helpes seperate boxes, maybe
                                "display": "flex",
                                "justify-content": "space-around",
                                "padding": "10px 10px 10px 10px"
                            },
                             #Six columns = half the row
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
                        #Box shadow gives a light border
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 20px"
                    },
                    #Take up the whole row
                    className="row"
                ),
            #Seperate the motor controls for each motor
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
                        #A slider to control the motor speed
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
            ],
                style={
                    "align-items": "center",
                    "border": "1px solid #2a3f5f",
                    "border-radius": "4px",
                    #'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                    "padding": "10px 10px 10px 20px"
                },
                #Direct control box takes a third of the page
                className="four columns"
            ),
            html.Div([
                #A box to callback the srt's current direction
                html.Div([
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
                        ),
                        html.Div([
                            html.Div([
                                "Azimuth:  "
                            ],
                                style={
                                    'textAlign': 'right'
                                },
                                className="three columns"
                            ),
                            html.Div(
                                id="azimuth",
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
                    #Gets half the row, shares with Input direction
                    className="six columns"
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
                        #Reports alt az of ra and dec user input
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
                                id="alt",
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
                                id="az",
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
                    className="six columns"
                )                    
            ],
                style={
                    "align-items": "center",
                    "border": "1px solid #2a3f5f",
                    "border-radius": "4px",
                    #'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                    "padding": "20px 20px 20px 20px"
                },
                className="eight columns"
            ),
            html.Div([
                #User input object
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
                        type='text',
                        className="ten columns"
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
                    className='five columns'
                ),

                html.Div([
                    dcc.Input(
                        id='DEC', 
                        value='12d24m35s', 
                        type='text',
                        className="ten columns"
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
                    className='five columns'
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
                    "border": "1px solid #2a3f5f",
                    "border-radius": "4px",
                    "position": "relative",
                    "marginTop": "5%",
                    "marginBottom": "5%",
                    "padding": "10px 10px 10px 10px"
                    },
                className="eight columns"
            ),
            html.Div([
                #Select how to observe
                html.Div([
                        html.H3(
                            "Observing Method"
                        )
                    ], 
                        className='Title'
                    ),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6(
                                "Method Select"
                            )
                        ], 
                            className='Title'
                        ),
                        #Pick the method
                        dcc.RadioItems(
                            id="select",
                            options=[
                                {'label': 'Go To', 'value': 'Goto'},
                                {'label': 'Tracking', 'value': 'Track'},
                                {'label': 'Scan', 'value': 'Scan'}
                            ],
                            value='Goto'
                        )
                    ],
                        style={
                            "align-items": "center",
                            'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                            "padding": "10px 10px 5px 10px"
                        },
                        className="six columns"
                    ),
                    html.Div([
                        html.Div([
                            html.H6(
                                "Tracking Setting"
                            )
                        ], 
                            className='Title'
                        ),
                        dcc.Dropdown(
                            id='tracker',
                            options=[
                                {'label': '20 s', 'value': '20s'},
                                {'label': '40 s', 'value': '40s'},
                                {'label': '1 min', 'value': '1min'},
                                {'label': '2 min', 'value': '2min'},
                                {'label': '5 min', 'value': '5min'},                                                                                                
                            ],
                            value='1min'
                        ),
                        html.Div([
                            #Placed for spacing, can probably get rid of
                            dcc.RadioItems(
                                options=[
                                    {'label': 'this is a place holder', 'value': 'val'}
                                ]
                            )
                            ],
                                style={
                                    "visibility": "hidden"
                                }
                        )
                    ],
                        style={
                            "align-items": "center",
                            'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                            "padding": "10px 10px 10px 10px"
                        },
                        className="six columns"
                    )
                ],
                    className="row"
                ),
                html.Div([
                    #Boxes for specific method instructions
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H6(
                                    "Scan"
                                )
                            ], 
                                className='Title'
                            ),
                            dcc.RadioItems(
                                id='scanner',
                                options=[
                                    {'label': 'Full Sky', 'value': 'FullSky'},
                                    {'label': 'Object', 'value': 'Obj'}
                                ],
                                value='Obj'
                            )
                        ],
                            className="four columns"
                        ),
                        html.Div([
                            html.Div([
                                html.H6(
                                    "Box Size"
                                )
                            ], 
                                className='Title'
                            ),
                            html.Div([
                                dcc.Input(
                                    id='boxSize', 
                                    value='10', 
                                    type='text',
                                    className="five columns"
                                ),
                                html.H5(
                                    "°", 
                                    style={
                                        "paddingRight": "50%",
                                        "textAlign": "right"
                                    }
                                )
                            ]
                            )
                    ],
                        className="four columns"
                    ),
                    html.Div([
                        html.Div([
                            html.H6(
                                "Scan Speed"
                            )
                        ], 
                            className='Title'
                        ),
                        html.Div([
                            dcc.Input(
                                id='scanSpeed', 
                                value='10', 
                                type='text',
                                className="five columns"
                            ),
                            html.H5(
                                "°/min", 
                                style={
                                    "paddingRight": "30%",
                                    "textAlign": "right"
                                }
                            )
                        ], 
                            className='row'
                        )
                ],
                    className="four columns"
                )
                ],
                    style={
                        "align-items": "center",
                        'boxShadow': '1px 1px 1px 1px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 10px"
                    },
                    className="row"
                )
                ],
                    className="row"
                )
            ],
                style={
                        "align-items": "center",
                        "border": "1px solid #2a3f5f",
                        "border-radius": "4px",
                        #'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                        "padding": "10px 10px 10px 10px"
                    },
                className="eight columns"
            ),
            html.Div([
                html.Div(id='go-home-button-count'),
                html.Div(id='stop-button-count'),
                html.Div(id='alt-for-button-count'),
                html.Div(id='alt-rev-button-count'),
                html.Div(id='az-for-button-count'),
                html.Div(id='az-rev-button-count'),
                html.Div(id='placeholder'),
                dcc.Interval(
                    id='refresher',
                    interval=1000),
                dcc.Interval(
                    id='refresher2',
                    interval=10000)
            ],
                style={
                    "visibility": "hidden"
                }
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

#I think this getting deleted
@app.callback(
    Output(component_id='tracker', component_property='disabled'),
    [Input(component_id='select', component_property='value')]
)

def stateFunc1(selection):
    if selection == 'Track':
        return False
    else:
        return True

#Box Size will be disabled if Scan 
@app.callback(
    Output(component_id='boxSize', component_property='disabled'),
    [Input(component_id='select', component_property='value'),
    Input(component_id='scanner', component_property='value')]
)

def stateFunc3(selection, selection2):
    if selection == 'Scan' and selection2 == 'Obj':
        return False
    else:
        return True

#ScanSpeed will be disabled if scan is not on
@app.callback(
    Output(component_id='scanSpeed', component_property='disabled'),
    [Input(component_id='select', component_property='value')]
)

def stateFunc4(selection):
    if selection == 'Scan':
        return False
    else:
        return True

# Connects RA and Dec coordinates to an Alt and Az output
@app.callback(
    Output(component_id='alt', component_property='children'),
    [Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value'),
     Input(component_id='go-button', component_property='n_clicks')]
)

def output_alt(RA, DEC, clicks):
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
    Output(component_id='az', component_property='children'),
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
        #Need to keep track of clicks(still not sure if necessary)
        homeprev = homeprev + 1

#Button to Stop motors
@app.callback(
    Output(component_id='stop-button-count', component_property='children'),
    [Input(component_id='stop-button', component_property='n_clicks')]
)

def StopButton(stop_clicks):
    #String to be sent to the Arduino
    this_str = "<0,0>"
    #Sends string to the Arduino
    ser1.write(str.encode(this_str))

#Alt Direct Motor Control begins now
@app.callback(
    Output(component_id='alt-for-button-count', component_property='children'),
    [Input(component_id='alt-forward-button', component_property='n_clicks'),
    dash.dependencies.Input('alt-slider', 'value')]
)

#Changes the motor speed based on the slider
def AltForButton(alt_for_clicks, speed_alt):
    global altforprev
    if alt_for_clicks > altforprev:
        #The speed component is 3 spaces, the if statements allows for a 0 to come before a
        if speed_alt < 100:
            this_str = "<0,1,9999,0{}>".format(speed_alt)
        if speed_alt == 100:
            this_str = "<0,1,9999,{}>".format(speed_alt)
        if speed_alt < 10:
            this_str = "<0,1,9999,00{}>".format(speed_alt)
        ser1.write(str.encode(this_str))
        altforprev = altforprev + 1

@app.callback(
    Output(component_id='alt-rev-button-count', component_property='children'),
    [Input(component_id='alt-reverse-button', component_property='n_clicks'),
    dash.dependencies.Input('alt-slider', 'value')]
)

def AltRevButton(alt_rev_clicks, speed_alt):
    global altrevprev
    if alt_rev_clicks > altrevprev:
        if speed_alt < 100:
            this_str = "<0,2,9999,0{}>".format(speed_alt)
        if speed_alt == 100:
            this_str = "<0,2,9999,{}>".format(speed_alt)
        if speed_alt < 10:
            this_str = "<0,2,9999,00{}>".format(speed_alt)
        ser1.write(str.encode(this_str))
        altrevprev = altrevprev + 1

#Control motor speed for direct control
@app.callback(
    dash.dependencies.Output('speed-control-alt', 'children'),
    [dash.dependencies.Input('alt-slider', 'value')])

#This will only work up to 99
def AltSpeed(speed_alt):
    return 'PWM Duty Cycle = "{}"'.format(speed_alt)

#Azimuth Direct Motor Control Begins now
@app.callback(
    Output(component_id='az-for-button-count', component_property='children'),
    [Input(component_id='az-forward-button', component_property='n_clicks'),
    dash.dependencies.Input('az-slider', 'value')]
)

def AzForButton(az_for_clicks, speed_az):
    global azforprev
    if az_for_clicks > azforprev:
        if speed_az < 100:
            this_str = "<0,1,9999,0{}>".format(speed_az)
        if speed_az == 100:
            this_str = "<0,1,9999,{}>".format(speed_az)
        if speed_az < 10:
            this_str = "<0,1,9999,00{}>".format(speed_az)
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
        if speed_az < 100:
            this_str = "<0,2,9999,0{}>".format(speed_az)
        if speed_az == 100:
            this_str = "<0,2,9999,{}>".format(speed_az)
        if speed_az < 10:
            this_str = "<0,2,9999,00{}>".format(speed_az)
        ser1.write(str.encode(this_str))
        azrevprev = azrevprev + 1

@app.callback(
    dash.dependencies.Output('speed-control-az', 'children'),
    [dash.dependencies.Input('az-slider', 'value')])

def AltSpeed(speed_az):
    return 'PWM Duty Cycle = "{}"'.format(speed_az)

#Callable function for converting decimals to rounded degree, minutes, seconds
def degreeSpliterRounder(angle):
    #Doesn't work for negatives
    is_positive = angle >= 0
    angle = abs(angle)
    #Actual seperation
    minutes,seconds = divmod(angle*3600,60)
    degrees,minutes = divmod(minutes,60)
    #Convert back to negative
    degrees = degrees if is_positive else -degrees
    #Round and return
    deg =round(degrees)
    mins = round(minutes)
    sec = round(seconds)
    return deg, mins, sec

#This is to output the motors actual location
@app.callback(
    Output(component_id='altitude', component_property='children'),
    [Input(component_id='refresher', 
          component_property='n_intervals')]
)

def motorLocation(delay):
    global motAz
    #Request count from Arduino
    ser1.write(str.encode("<9>"))
    #Sometimes the read isn't timed right so allow an exception
    try:
        data =ser1.readline().decode('ascii')
        data1 = data.split(" ")
    except serial.serialutil.SerialException:
        return motAz
    #A partial read will give a bad number so dont process it
    try:
        location = int(data1[0])
    except ValueError:
        return motAz
    #Check which side of the gear the dish is on
    #Count is limited to about 2006 pulses
    if location <= 1003:
        #Convert to degrees
        azimuthDec = 90 * location / 1003
        #round
        az_deg = round(azimuthDec)
        #make string for return
        motAz = "{}°".format(az_deg)
        #reset data
        data = ''
        return motAz
    if location > 1003:
        azimuthDec = 90 - 90 * (location - 1003) / 1003
        az_deg = round(azimuthDec)
        motAz = "{}°".format(az_deg)
        data = ''
        return motAz
    #Continue returning previous MotAz
    else:
        return motAz

@app.callback(
    Output(component_id='azimuth', component_property='children'),
    [Input(component_id='refresher', 
          component_property='n_intervals')]
)

def motorLocation(delay):
    global motAz
    ser1.write(str.encode("<9>"))
    try:
        data =ser1.readline().decode('ascii')
        data1 = data.split(" ")
    except serial.serialutil.SerialException:
        return motAz
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

@app.callback(
    Output('graph', 'figure'),
    [Input(component_id='refresher2', 
          component_property='n_intervals'),
    Input(component_id='solarsystem', component_property='value'),
    Input(component_id='RA', component_property='value'),
     Input(component_id='DEC', component_property='value')]
)

#Makes Graph with Sun, Moon and planets and trajectory of object of choice
def MakeGraph(delay, val, RA, DEC):
    #Need observation location
    Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
    #Preps altitude and observation time
    aa = AltAz(location=Winona, obstime=Time.now())
    #Array of bodies to observe in the solar system
    Bodies = np.array(['sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'moon'])
    #Create blank arrays to update in for loop
    BodyAz = np.array([])
    BodyAlt = np.array([])
    #Gets the Alt and Az for bodies in seperate arrays
    for i in Bodies:
        Bodycrd = get_body(i, Time.now(), Winona).icrs
        BodyAlt = np.append(BodyAlt,Bodycrd.transform_to(aa).alt.deg)
        BodyAz = np.append(BodyAz,Bodycrd.transform_to(aa).az.deg)
    #Names for displaying on graph
    SolarSystemNames = np.array(['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Moon'])
    #Unique sizes for different bodies
    SolarSizes = [25, 10, 10, 10, 15, 15, 15, 15, 25]
    #Unique colors for different bodies
    SolarColors = ['yellow', 'grey', 'yellow', 'red', 'red', 'orange', 'blue', 'blue', 'grey']
    #Call for object user is observing
    BodAz1, BodAlt1, BodAz2, BodAlt2 = getAltAz(val, RA, DEC)
    directions = ['N', 'E', 'S', 'W']
    directLoc = [0, 90, 180, 270]
    return {
        'data': [
                #Object observing
                go.Scatter(
                    name="Future",
                    x=BodAz1,
                    y=BodAlt1,
                ),
                #Trajectory of object observing
                go.Scatter(
                    name="Past",
                    x=BodAz2,
                    y=BodAlt2
                ),
                #Coordinates
                go.Scatter(
                    name="Sun",
                    x=BodyAz,
                    y=BodyAlt,
                    mode='markers',
                    text=SolarSystemNames,
                    marker={
                        'size': SolarSizes,
                        'color': SolarColors
                    }
                )
                ],
        "layout": go.Layout(
            #Set range
            xaxis={
                "title": "Azimuth", 
                "range": [0,360], 
                "ticktext":directions, 
                "tickvals":directLoc},
            yaxis={"title": "Altitude", 'range': [0, 90]},
            margin={"l": 70, "b": 100, "t": 0, "r": 25},
        )
    }

#Call function for observing specified object
def getAltAz(val, RA, DEC):
    Winona = EarthLocation(lat='44.0554d', lon='-91.6664', height=202*u.m)
    #Predefined objects
    if val != 'object':
        Body = get_body(val, Time.now(), Winona).icrs
    #User specified object
    else:
        Body = SkyCoord(RA, DEC, frame='icrs')
    
    timeNow=Time.now()
    #Array for 24 hour period
    delta_hours = np.linspace(0, 12, 100)*u.hour
    full_night_times1 = timeNow + delta_hours
    full_night_times2 = timeNow - delta_hours
    #Creates array of alt az locations for this time
    full_night_aa_frames1 = AltAz(location=Winona, obstime=full_night_times1)
    full_night_aa_coos = Body.transform_to(full_night_aa_frames1).icrs
    #Location objects been
    BodAlt1 = Body.transform_to(full_night_aa_frames1).alt.deg
    BodAz1 = Body.transform_to(full_night_aa_frames1).az.deg
    #Location object will be (hopefully)
    full_night_aa_frames2 = AltAz(location=Winona, obstime=full_night_times2)
    full_night_aa_coos = Body.transform_to(full_night_aa_frames2).icrs

    BodAlt2 = Body.transform_to(full_night_aa_frames2).alt.deg
    BodAz2 = Body.transform_to(full_night_aa_frames2).az.deg
    #
    return BodAz1, BodAlt1, BodAz2, BodAlt2

if __name__ == '__main__':
    app.run_server(debug=True)
