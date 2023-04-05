import pandas as pd
import webbrowser
from dash import Dash, dcc, html, dash_table, Input, Output, State
import subprocess

df_ledgie = pd.read_csv('accounts_reference.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children="Journal entry for yesterday's data", style={'textAlign': 'center'}),
    
    html.Div([
        html.P('Welcome JR', style={'textAlign': 'center'}),
        html.P("Please click submit if the data looks ok", style={'textAlign': 'center'})
    ]),

    dash_table.DataTable(
        df_ledgie.to_dict('records'), 
        [{"name": i, "id": i} for i in df_ledgie.columns],
        style_table={'height': 400, 'overflowX': 'auto'} ,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        fixed_rows={'headers': True},
        style_cell={'textAlign': 'left', 'textOverflow': 'ellipsis', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df_ledgie.to_dict('records')
        ],
        tooltip_duration=None

     ), # defaults to 500,

    html.Div([
        html.Button('Submit', id='submit-val', n_clicks=0, style={'textAlign': 'center'}) 
    ], style={'textAlign': 'center'})
])

# Open the Dash URL in the default browser when the script is run
webbrowser.open('http://127.0.0.1:8050/')

@app.callback(
    Output('submit-val', 'n_clicks'),
    [Input('submit-val', 'n_clicks')]
)

def run_main_script(n_clicks):
    if n_clicks > 0:
        subprocess.call(['python3', 'quickbooks_auth.py'])
    return n_clicks



if __name__ == "__main__":
    app.run_server(debug=True)
