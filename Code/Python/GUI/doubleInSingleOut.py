import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(className='row', 
             children=[
            html.Div([
                dcc.Input(id='my-id', 
                          value='initial value', 
                          type='text'),
                html.Div(id='my-div')], 
                className='three columns'),

            html.Div([
                dcc.Input(id='new-my-id', 
                          value='initial value', 
                          type='text'),
                html.Div(id='new-my-div')],
                className='three columns')
             ])
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value'),
     Input(component_id='new-my-id', component_property='value')]
)

def update_output_div(input_value, new_input_value):
    return 'You\'ve entered "{}"'.format(input_value + ',' + new_input_value)

if __name__ == '__main__':
    app.run_server(debug=True)