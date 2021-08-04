#covid 19 dashboard project
#import library
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as doc
from dash.dependencies import Input, Output

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

#read csv file
patient = pd.read_csv("IndividualDetails.csv")
total = patient.shape[0]
active = patient[patient['current_status'] == "Hospitalized"].shape[0]
recovered = patient[patient['current_status'] == "Recovered"].shape[0]
deaths = patient[patient['current_status'] == "Deceased"].shape[0]

main=pd.read_csv('covid_19_india.csv')
main['total']=main['ConfirmedIndianNational'] + main['ConfirmedForeignNational']
main['total']=np.cumsum(main['total'].values)

age=pd.read_csv('AgeGroupDetails.csv')

options = [
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#create layout
app.layout = html.Div([
    html.H1("Corona Virus Pendemic", style = {"color":'#fff', 'text-align':'center', 'margin':'10px'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases"),
                    html.H4(total)
                ], className = "card-body text-light")
            ], className = "card bg-danger")
        ], className = "col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases"),
                    html.H4(active)
                ], className = "card-body text-light")
            ], className = "card bg-info")
        ], className = "col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered"),
                    html.H4(recovered)
                ], className = "card-body text-light")
            ], className = "card bg-warning")
        ], className = "col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths"),
                    html.H4(deaths)
                ], className = "card-body text-light")
            ], className = "card bg-success")
        ], className = "col-md-3")
    ], className = "row"),
    html.Div([
        #start 2nd row
        html.Div([
            html.Div([
                html.Div([
                    doc.Graph(id='Line Plot',
                              figure={'data':[go.Scatter(x=main['Date'], y=main['total'],mode='lines')],
                                      'layout':go.Layout(title='Day by Day Analysis',xaxis={'title':'Date'},yaxis={'title':'Number of Cases'})})
                ], className='card-body')
            ],className='card')
        ], className='col-md-8'),
        html.Div([
            html.Div([
               html.Div([
                   doc.Graph(id='pie',
                             figure={'data':[go.Pie(labels=age['AgeGroup'],values=age['TotalCases'])],
                                     'layout':go.Layout(title='Age Distribution')})
               ], className='card-body')
            ], className="card")
        ], className='col-md-4')
        #end second row
    ], className = "row my-4"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    doc.Dropdown(id = 'picker', options = options, value = 'All' ),
                    doc.Graph(id = 'bar')
                ], className = "card-body")
            ], className = "card")
        ], className = "col-md-12")
    ], className = "row my-4")
], className = "container")

@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):
    if type == "All":
        patient_bar = patient['detected_state'].value_counts().reset_index()
        return {
            'data':[go.Bar(x = patient_bar['index'], y = patient_bar['detected_state'])],
            'layout':go.Layout(title = "state total count")
        }
    else:
        npat = patient[patient['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()
        return {
            'data':[go.Bar(x = pbar['index'], y = pbar['detected_state'])],
            'layout':go.Layout(title = "state total count")
        }
if __name__ == "__main__":
    app.run_server(debug = True)