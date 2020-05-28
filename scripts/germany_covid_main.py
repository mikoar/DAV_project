import plotly
import plotly.graph_objs as go
import pandas as pd
import sys

covid_germany = pd.read_csv("../data/germany_covid.csv")

fig = go.Figure()


fig.add_scatter(x=covid_germany.Date, y=covid_germany.Confirmed, name="Confirmed", mode='lines',
                    hovertemplate= 
                    "Date: %{x}<br>" + \
                    "Confirmed: %{y}<br>" + \
                    "<extra></extra>",
                    line=dict(width=2, color = "#1f77b4"))
fig.add_scatter(x=covid_germany.Date, y=covid_germany.Deaths, name="Deaths", mode='lines',
                    hovertemplate= "Deaths: %{y}<br><extra></extra>",
                    line=dict(width=2, dash="dash", color = '#d62728'))

fig.add_scatter(x=covid_germany.Date, y=covid_germany.Recovered, name="Recovered", mode='lines+markers', 
                    hovertemplate= "Recovered: %{y}<br><extra></extra>",
                    line=dict(width=2, color = '#2ca02c'))

fig.add_scatter(x=covid_germany.Date, y=covid_germany.Active, name="Active", mode='lines',
                    hovertemplate= "Active: %{y}<br><extra></extra>",
                    line=dict(width=2, dash="dot", color = '#9467bd'))

fig.add_scatter(x=covid_germany.Date, y=covid_germany["New cases"], name="Confirmed", mode='lines',
                    hovertemplate= 
                    "Date: %{x}<br>" + \
                    "Confirmed: %{y}<br>" + \
                    "<extra></extra>",
                    visible = False,
                    line=dict(width=2, color = "#1f77b4"))
fig.add_scatter(x=covid_germany.Date, y=covid_germany["New deaths"], name="Deaths", mode='lines',
                    hovertemplate= "Deaths: %{y}<br><extra></extra>", visible = False,
                    line=dict(width=2, dash="dash", color = '#d62728'))

fig.add_scatter(x=covid_germany.Date, y=covid_germany["New recovered"], name="Recovered", mode='lines+markers', 
                    hovertemplate= "Recovered: %{y}<br><extra></extra>", visible = False,
                    line=dict(width=2, color = '#2ca02c'))


updatemenus = list([
    dict(direction="right",
         type = "buttons",
        showactive=True,
        active=1,
         yanchor="top",
         x=0.14,
         y=1.05,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
                 args=[{'visible': [True]*4 + [False]*3},
                     {
                        'yaxis': {'type': 'log'}}]),
            dict(label='Linear Scale',
                 method='update',
                 args=[{'visible':[True]*4 + [False]*3},
                       {
                        'yaxis': {'type': 'linear'}}])
            ]),
        ),
    dict(direction="right",
         type = "buttons",
        showactive=True,
        active=1,
         yanchor="top",
         x=0.14,
         y=1.1,
         buttons=list([
            dict(label='Total',
                 method='update',
                 args=[
                     {'visible': [True]*4 + [False]*3},
                     {'title': 'Covid-19 total cases'}]),
            dict(label='Daily',
                 method='update',
                 args=[
                     {'visible': [False]*4 + [True]*3},
                       {'title': 'Covid-19 daily cases'}])
            ]),
        )
    
    ])


fig.update_layout(legend_title_text='Case type', hovermode="x", updatemenus=updatemenus)

fig.update_layout(
    title={
        'text': "Covid-19 cases",
        'x':0.5,
        'y':0.92,
        'xanchor': 'center',
        'yanchor': 'top',
        "font": {"size": 20}})

args = sys.argv
if len(args)>1:
    if args[1] == "1":
        name = args[0].split(".")[0]
        path = "../plots/"
        fig.write_html("{}{}.html".format(path, name))
        print("The plot was saved to {}{}.html".format(path, name))
    else:
        fig.show()
else:
    fig.show()




