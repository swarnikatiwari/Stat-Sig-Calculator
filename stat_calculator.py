import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact

app = dash.Dash()

#define colors to standardize color calls throughout the dashboard
colors = dict(background ='#111111', text='#008080')

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

ALLOWED_TYPES = ("number", "number")

app.layout = html.Div(
	[ html.H2("Statistical Significance Calculator", style={'textAlign':'center', 'color':colors['text']}),
	  html.Label("Control"),
	  dcc.Input(id='conversion_control', value='conversion', type='number',placeholder="Control Conversion"),
	  dcc.Input(id='sample_control', value='sample', type='number', placeholder="Control Sample"),
	  html.Br(),
	  html.Label("Test"),
	  dcc.Input(id='conversion_test', value='conversion', type='number', placeholder="Test Conversion"),
	  dcc.Input(id='sample_test', value='sample', type='number', placeholder="Test Sample"),
	  html.Div(id='ratio')
	]
)

@app.callback(
    Output(component_id='ratio', component_property='children'),
    [Input('conversion_test','value'),Input('sample_test','value'),
     Input('conversion_control','value'),Input('sample_control','value') ]
)
def update_output_div(conversion_test, sample_test,conversion_control, sample_control):
	b = (conversion_test/sample_test)*100
	a = (conversion_control/sample_control)*100
	obs = np.array([[sample_control, conversion_control],[sample_test,conversion_test]])
	g, p, dof, expctd = chi2_contingency(obs, correction = False)
	return """Control Conversion Rate is: %f and Test Conversion Rate is: %f
			\n The p-value of this test is: %f"""%(a, b, p)

if __name__ == '__main__':
	app.run_server()