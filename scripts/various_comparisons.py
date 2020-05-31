# %%
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import sys
import datetime

data = pd.read_csv("../data/covid_countries.csv")
data.sort_values(by='date', inplace=True)
dates = pd.DataFrame({'date': data.date.unique()})

data = pd.merge(dates, data, how="left", on=["date"]).fillna(0)


fig = make_subplots(specs=[[{"secondary_y": True}]])

primary_y = [
    "total_deaths_per_million",
    "total_cases_per_million",
    "population_density",
    "median_age",
    "gdp_per_capita",
    "extreme_poverty",
    "cvd_death_rate",
    "hospital_beds_per_100k",
    "population",
]

percent_y = [
    "aged_65_older",
    "aged_70_older",
    "diabetes_prevalence",
    "female_smokers",
    "male_smokers",
]

initially_visible = ["total_deaths_per_million"]

data_for_countries = data[data.date == data.date.max()].groupby(
    ["location"] + primary_y + percent_y).size().reset_index().drop(columns=[0])

# %%
for (columnName, columnData) in data_for_countries.loc[:, data_for_countries.columns != 'location'].iteritems():
    fig.add_bar(name=columnName,
                x=data_for_countries.location,
                y=columnData,
                visible='legendonly' if columnName not in initially_visible else True,
                secondary_y=columnName in primary_y,
                opacity=0.5 if columnName in primary_y else 1,
                hovertemplate="%{fullData.name}<br>" +
                "Country: %{x}<br>" +
                "Value: %{y}<br>" +
                "<extra></extra>")

fig.update_layout(
    title={
        'text': "Various comparisons",
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
