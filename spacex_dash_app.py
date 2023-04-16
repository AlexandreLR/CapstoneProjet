# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites_list_df = spacex_df["Launch Site"].unique()
sites_list = []
sites_list.append({'label':"All sites",'value':"ALL"})
for i in range(0,len(sites_list_df)):
    sites_list.append({'label':sites_list_df[i],'value':sites_list_df[i]})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=sites_list,
                                             value="ALL",
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=18000, step=1000,
                                                marks={0:'0',
                                                       1000:'1000',
                                                       2000:'2000',
                                                       3000:'3000',
                                                       4000:'4000',
                                                       5000:'5000',
                                                       6000:'6000',
                                                       7000:'7000',
                                                       8000:'8000',
                                                       9000:'9000',
                                                       10000:'10000',
                                                       11000:'11000',
                                                       12000:'12000',
                                                       13000:'13000',
                                                       14000:'14000',
                                                       15000:'15000',
                                                       16000:'16000',
                                                       17000:'17000',
                                                       18000:'1000',},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        fig = px.pie(filtered_df, values=filtered_df.groupby(["class"])["Flight Number"].count(), 
        names={0:"Failure",1:"Success"}, 
        title=f'Total success launches for {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              [Input(component_id='payload_slider', component_property='value')])
def get_scatter_chart(entered_site,payload_range):
    if entered_site == 'ALL':
        df_pm = spacex_df[(spacex_df["Payload Mass (kg)"]>=payload_range[0]) &
                          (spacex_df["Payload Mass (kg)"]<=payload_range[1])]
        fig = px.scatter(df_pm, x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",
        title='Total success launches by site')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df["Launch Site"]==entered_site) & 
                                (spacex_df["Payload Mass (kg)"]>=payload_range[0]) &
                                (spacex_df["Payload Mass (kg)"]<=payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",
        title='Total success launches by site')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
