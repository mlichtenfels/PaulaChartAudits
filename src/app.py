import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash()


def f(x):
    if x == 'Yes':
        return 1.0
    elif x == 'No':
        return 0
    else:
        return np.nan

months = [('09', 'Sept'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]
for i,m in enumerate(months):
    file_path = 'ChartAudits2017{0}.csv'.format(m[0])
    df = pd.read_csv(file_path).replace(np.nan, '', regex=True)
    df = df.loc[:, 'Home Medication/Allergies reconciled day of surgery': 'Care Plan Interventions Completed >> Phase II']
    df = df.applymap(f)
    df = pd.DataFrame(df.mean(axis=0), columns=[m[1]])
    df = df * 100
    if m[0] != '09':
        df1 = df1.join(df, lsuffix=" {}".format(months[i-1][1]), rsuffix=" {}".format(m[1]))
    else:
        df1 = df[:].copy()
df1.fillna(0, inplace=True) #won't plot if I insert text such as 'NA'

df1.rename(index=
{
'Home Medication/Allergies reconciled day of surgery': 'Med/Allergy Rec',
 'Preop checklist completed': 'Preop Checklist',
 'Pre-procedure verification co-signed': 'Verification Co-signed',
 'H&P updated with correct phrase prior to surgery': 'H&P Updated',
 'Implants documented (must include lot number, site, and expiration date)': 'Implants Doc',
 'Wound class documented': 'Wound Class Doc',
 'Temperature > 96.8 degrees F': 'Temp > 96.8',
 'If temperature < 96.8, warming interventions documented': 'Temp < 96.8 Int Doc',
 'Repeat temp with second set of vital signs (PACU only)': 'Repeat Temp',
 'Post-anesthesia note/sign-out documented': 'Post-Anesth Sign-Out',
 'Brief operative note completed by surgeon': 'Brief Op Note',
 'Pain documented: >> In Preop': 'Pain - Preop',
 'Pain documented: >> Admission to Phase I': 'Pain Adm Ph I',
 'Pain documented: >> Discharge from Phase I': 'Pain Dis Ph I',
 'Pain documented: >> Admission to Phase II': 'Pain Adm Ph II',
 'Pain documented: >> Discharge from Phase II': 'Pain Dis Ph II',
 'Pain score documented within 60 minutes of pain intervention': 'Pain - Int',
 'Care Plan Interventions Completed >> Preop': 'Care Plan Preop',
 'Care Plan Interventions Completed >> Phase I': 'Care Plan Ph I',
 'Care Plan Interventions Completed >> Phase II': 'Care Plan Ph II'
}, inplace=True)

df2 = df1.round().astype(int)
df3 = df2.reset_index().rename(columns={'index': 'Category'})

def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )


app.layout = html.Div([
    html.Div([
     dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'September', 'value': 'Sept'},
            {'label': 'October', 'value': 'Oct'},
            {'label': 'November', 'value': 'Nov'},
            {'label': 'December', 'value': 'Dec'}
        ],
        value='Dec'
    )], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
    dcc.Graph(
        id='my-chart',
        figure={
            'data': [
                {'x': df2.index.tolist(), 'y': df2['Dec'], 'type': 'bar'}
            ],
            'layout': {
                 'title': 'December Chart Audits'
            }
            }
        )
    ], style={'display': 'inline-block', 'width': '60%'}),
    html.Div([
    html.H4(children='Chart Audits By Month'),
    generate_table(df3)
])

    ])

@app.callback(Output('my-chart', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    return {
        'data': [{
            'x': df2.index.tolist(),
            'y': df2[selected_dropdown_value],
            'type': 'bar'
        }],
        'layout': {
                 'title': '{} Chart Audits'.format(selected_dropdown_value)}
    }

if __name__ == '__main__':
    app.run_server(debug=True)