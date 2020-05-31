# %%
import plotly.graph_objs as go
import pandas as pd
import sys
import datetime

data = pd.read_csv("../data/number-of-covid-19-tests-per-confirmed-case-bar-chart.csv")
data.Date = data.Date.apply(lambda date: str(datetime.datetime.strptime(date, "%b %d, %Y")))
data.sort_values(by='Date', inplace=True)
data = data[data.Entity.isin(["Germany", "Poland", "United States", "Italy", "Russia", "Sweden", "Switzerland"])]
dates = pd.DataFrame({'Date': data.Date.unique()})

data = pd.merge(dates, data, how="left", on=["Date"]).fillna(0)


fig = go.Figure()

for country, data_for_country in data.groupby("Entity"):

    fig.add_scatter(x=data_for_country.Date, y=data_for_country.Tests, name=country, mode='lines+markers',
                    hovertemplate="Date: %{x}<br>" +
                    "Tests: %{y}<br>" +
                    "<extra></extra>",
                    line=dict(width=2))

fig.update_layout(
    title={
        'text': "Tests per confirmed case",
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
