# %%
import plotly.graph_objs as go
import pandas as pd
import sys
import datetime
import plotly.express as px

data = pd.read_csv("../data/covid_countries.csv")
data.sort_values(by='date', inplace=True)
# data = data[data.Entity.isin(["Germany", "Poland", "United States", "Italy", "Russia", "Sweden", "Switzerland"])]
dates = pd.DataFrame({'date': data.date.unique()})

data = pd.merge(dates, data, how="left", on=["date"]).fillna(0)

# fig = px.scatter(data, x="date", y="total_cases_per_million", color = "location")

fig = go.Figure()

for country, data_for_country in data.groupby("location"):

    fig.add_scatter(x=data_for_country.date, y=data_for_country.total_cases_per_million, name=country, mode='lines+markers',
                    color_discrete_sequence=px.colors.qualitative.Plotly, 
                    hovertemplate="Date: %{x}<br>" +
                    "Total cases per million: %{y}<br>" +
                    "<extra></extra>",
                    line=dict(width=2))
    
    fig.add_scatter(x=data_for_country.date, y=data_for_country.new_cases_per_million, name=country, mode='lines+markers',
                    color_discrete_sequence=px.colors.qualitative.Plotly, 
                    visible = False, 
                    hovertemplate="Date: %{x}<br>" +
                    "Total cases per million: %{y}<br>" +
                    "<extra></extra>",
                    line=dict(width=2))
    
    
    
updatemenus = list([
    dict(direction="right",
         type = "buttons",
        showactive=True,
        active=1,
         yanchor="top",
         x=0.2,
         y=1.2,
         buttons=list([
            dict(label='Total',
                 method='update',
                 args=[
                     {'visible': [True, False]*7},
                     {'title': 'Covid-19 total cases'}]),
            dict(label='Daily',
                 method='update',
                 args=[
                     {'visible': [False, True]*7},
                       {'title': 'Covid-19 daily cases'}])
            ]),
        )
    
    ])


fig.update_layout(legend_title_text='Country', hovermode="x", updatemenus=updatemenus)


fig.update_layout(
    title={
        'text': "Total cases per million",
        'x': 0.5,
        'y': 0.92,
        'xanchor': 'center',
        'yanchor': 'top',
        "font": {"size": 20}})

args = sys.argv
if len(args) > 1:
    if args[1] == "1":
        name = args[0].split(".")[0]
        path = "../plots/"
        fig.write_html("{}{}.html".format(path, name))
        print("The plot was saved to {}{}.html".format(path, name))
    else:
        fig.show()
else:
    fig.show()
