import plotly.express as px
import pandas as pd
import sys
from functools import reduce

data = pd.read_csv("../data/RKI_COVID19.csv")

data_pop = data.groupby(["Meldedatum","Geschlecht", "Altersgruppe"]).size().reset_index(name='counts')
data_pop.columns = ["date", "sex", "age_group", "counts"]
data_pop = data_pop.loc[(data_pop.age_group!="unbekannt") & (data_pop.sex!="unbekannt"), :]

df1 = pd.DataFrame({"sex" : ["W", "M"], "key": 0})
df2 = pd.DataFrame({'age_group': ['A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 'A80+'], "key": 0})
df3 = pd.DataFrame({'date': data_pop.date.unique(), "key": 0})

grid = reduce(lambda left,right: pd.merge(left,right,how='outer'), [df1, df2, df3]).drop("key", axis = 1)
total_pop = pd.merge(grid, data_pop, how = "left", on = ["age_group", "sex", "date"]).fillna(0)

total_pop['no_csum'] = total_pop.groupby(['sex', 'age_group'])['counts'].cumsum()

fig = px.bar(total_pop, x="age_group", y="no_csum",  color="sex", barmode='group', animation_frame="date"
             ,labels={"age_group": "Age Group", "no_csum": "Number of people diagnosed with Covid-19"}
            )
fig.update_yaxes(range=[0, 30000])
fig.update_layout(barmode='group', xaxis={'categoryarray':["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79", "A80+"], 'type': 'category'},
                 title = {'text': 'Cumulated cases of Covid-19 by sex and age group', 'xanchor': "center", 'x':0.5})

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