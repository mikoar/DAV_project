# %%
import plotly.graph_objs as go
import pandas as pd
import sys
import datetime

data = pd.read_csv("../data/covid_countries.csv")
data.sort_values(by='date', inplace=True)
# data = data[data.Entity.isin(["Germany", "Poland", "United States", "Italy", "Russia", "Sweden", "Switzerland"])]
dates = pd.DataFrame({'date': data.date.unique()})

data = pd.merge(dates, data, how="left", on=["date"]).fillna(0)

fig = go.Figure()

for country, data_for_country in data.groupby("location"):

    fig.add_scatter(x=data_for_country.date, y=data_for_country.new_deaths_per_million, name=country, mode='lines+markers',
                    hovertemplate="Date: %{x}<br>" +
                    "Daily deaths per million: %{y}<br>" +
                    "<extra></extra>",
                    line=dict(width=2))
    

fig.update_layout(legend_title_text='Country')


fig.update_layout(
    title={
        'text': "Daily deaths per million",
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
