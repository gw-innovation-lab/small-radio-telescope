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
    html.Div(className='row', 
             children=[
            html.Div([
                dcc.Input(id='my-id', 
                          value='240d20m30s', 
                          type='text'),
                html.H5("Right Ascension", style={"textAlign": "bottom"})
                ], 
                className='three columns'),

            html.Div([
                dcc.Input(id='new-my-id', 
                          value='12d24m35s', 
                          type='text'),
                html.H5("Declenation", style={"textAlign": "center"})
                ],
                className='three columns'),
            html.Div([
                daq.StopButton(
                    id="go-button",
                    buttonText="Go",
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                    className="three columns",
                    n_clicks=0,
                    )
             ]),
    html.Div(id='my-div')
    ])
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value'),
     Input(component_id='new-my-id', component_property='value'),
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
        az = sky_locRAD.transform_to(aa).az.deg
        prev_clicks = prev_clicks + 1
        return 'Altittude: "{}"  Azimuth: "{}"'.format(alt, az)
    else:
        return 'You\'ve entered "{}"'


if __name__ == '__main__':
    app.run_server(debug=True)