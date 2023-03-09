import pandas as pd
from dash import Dash, dcc, html, dash_table

df_reference = pd.read_csv('accounts_reference.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children= "Journal entry for yesterday's data"),
    
    html.Div([
    html.P('Dash converts Python classes into HTML'),
    html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ]),

    dash_table.DataTable(
    df_reference.to_dict('records'), 
    [{"name": i, "id": i} for i in df_reference.columns],
    style_table = {'height': 400, 'overflowX': 'auto'} ,
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    },
    fixed_rows = {'headers': True},
    style_cell={'textAlign': 'left', 'textOverflow': 'ellipsis', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
    tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in df_reference.to_dict('records')
    ],
    tooltip_duration=None

     ) # defaults to 500

    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
