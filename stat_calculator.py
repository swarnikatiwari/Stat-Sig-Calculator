import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
from flask import Flask
import pandas as pd
import math
import plotly.express as px
import scipy.stats as scs

#app = dash.Dash()
server = Flask('my app')

# define colors to standardize color calls throughout the dashboard
colors = dict(background='#111111', text='#008080')

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

def graph_data(conv_A, total_A, conv_B, total_B):
    max_conv = max(conv_A, conv_B)
    if max_conv%2 ==0:
        range = max_conv
    else:
        range = max_conv+1
    #to specify line space ranges for the AB binomial graph
    half_value = math.ceil(max_conv/2)

    xA = np.linspace(conv_A- (half_value-1),conv_A+ half_value, range)
    yA = scs.binom(total_A, (conv_A/total_A)).pmf(xA)
    xB = np.linspace(conv_B- (half_value-1),conv_B+ half_value, range)
    yB = scs.binom(total_B, (conv_B/total_B)).pmf(xB)

    #data frame for graph
    display_data = pd.DataFrame(xA)
    display_data.columns =['x']
    display_data['y'] =yA
    display_data['test_group'] = 'A'
    data2 = pd.DataFrame(xB)
    data2.columns =['x']
    data2['y'] =yB
    data2['test_group'] = 'B'
    display_data = display_data.append(data2, ignore_index=True)
    display_data.columns =['converted', 'probability', 'test_group']
    return display_data

#set up flask server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
# server = app.server

# print(server)

ALLOWED_TYPES = ("number", "number")

app.layout = html.Div(
        [html.H2("Statistical Significance Calculator", style={'textAlign': 'center', 'color': colors['text']}),
         html.Label("A"),
         dcc.Input(id='conversion_control', value=100, type='number', placeholder='Control Conversion', debounce=True),
         dcc.Input(id='sample_control', value=1000, type='number', placeholder='Control Sample', debounce=True),
         html.Br(),
         html.Label("B"),
         dcc.Input(id='conversion_test', value=150, type='number', placeholder='Test Conversion', debounce=True),
         dcc.Input(id='sample_test', value=1000, type='number', placeholder='Test Sample', debounce=True),
         html.Div(id='ratio', style={'textAlign': 'center'}),
         # create a default graph
         html.Br(),
         html.P("Visual representation of the conversion probabilities of each test group:", style={'textAlign': 'center'}),
         html.Br(),
         dcc.Graph(id='AvB', style={"width": "75%", "display": "inline-block", "align":"center"})
         ]
)


@app.callback(
        [Output(component_id='ratio', component_property='children'),
        Output(component_id='AvB', component_property='figure')],
        [Input('conversion_test', 'value'), Input('sample_test', 'value'),
         Input('conversion_control', 'value'), Input('sample_control', 'value')]
)

def update_output_div(conversion_test, sample_test, conversion_control, sample_control):
    b = (float(conversion_test) / float(sample_test)) * 100
    a = (float(conversion_control) / float(sample_control)) * 100
    obs = np.array([[sample_control, conversion_control], [sample_test, conversion_test]])
    g, p, dof, expctd = chi2_contingency(obs, correction=False)

    graph_df = graph_data(conversion_control, sample_control,conversion_test, sample_test)
    #fig = px.bar(graph_df[graph_df["test_group"]=='A'], x="converted", y="probability", color="test_group")
    #fig.add_trace(px.bar(graph_df[graph_df["test_group"]=='B'], x="converted", y="probability", color="test_group"))
    # a = 0
    # b = 1
    # p = 2
    return """A Conversion Rate is: %.2f %% and B Conversion Rate is: %.2f %% \n
			 The p-value of this test is: %f""" % (a, b, p), px.bar(graph_df, x="converted", y="probability", color="test_group", barmode='group')


if __name__ == '__main__':
    app.run_server()
