import plotly.express as px
import pandas as pd
import sys
from functools import reduce

data = pd.read_csv("../data/RKI_COVID19.csv")

federa_state_dict = {
    "Baden-Württemberg": "Baden-Württemberg",
    "Bayern": "Bavaria",
    "Berlin": "Berlin",
    "Brandenburg": "Brandenburg",
    "Bremen": "Bremen",
    "Hamburg": "Hamburg",
    "Hessen": "Hesse",
    "Mecklenburg-Vorpommern": "Mecklenburg-Western Pomerania",
    "Niedersachsen": "Lower Saxony",
    "Nordrhein-Westfalen": "North Rhine Westphalia",
    "Rheinland-Pfalz": "Rhineland-Palatinate",
    "Saarland": "Saarland",
    "Sachsen-Anhalt": "Saxony-Anhalt",
    "Sachsen": "Saxony",
    "Schleswig-Holstein": "Schleswig Holstein",
    "Thüringen": "Thuringia"
}

federa_state_neighbours_dict = {
    "Baden-Württemberg": "Switzerland/France",
    "Bavaria": "Czech Republic/Austria",
    "Berlin": "inner",
    "Brandenburg": "Poland",
    "Bremen": "inner",
    "Hamburg": "inner",
    "Hesse": "inner",
    "Mecklenburg-Western Pomerania": "Poland",
    "Lower Saxony": "Netherlands",
    "North Rhine Westphalia": "Netherlands",
    "Rhineland-Palatinate": "France/Luxembourg",
    "Saarland": "France",
    "Saxony-Anhalt": "inner",
    "Saxony": "Poland/Czech Rebublic",
    "Schleswig Holstein": "Denmark",
    "Thuringia": "inner"
}

data["federal_state"] = [federa_state_dict[x] for x in data.Bundesland]
data_pop = data.groupby(["Meldedatum","federal_state"]).size().reset_index(name='counts')
data_pop.columns = ["date", "federal_state",  "counts"]

df1 = pd.DataFrame({"federal_state" : data_pop.federal_state.unique(), "key": 0})
df2 = pd.DataFrame({'date': data_pop.date.unique(), "key": 0})

grid = reduce(lambda left,right: pd.merge(left,right,how='outer'), [df1, df2]).drop("key", axis = 1)
total_pop = pd.merge(grid, data_pop, how = "left", on = ["federal_state", "date"]).fillna(0)
total_pop['no_csum'] = total_pop.groupby(['federal_state'])['counts'].cumsum()
total_pop['neighbour'] = [federa_state_neighbours_dict[x] for x in total_pop.federal_state]

fig = px.bar(total_pop, x="federal_state", y="no_csum",  color = "neighbour"
             ,color_discrete_sequence = ["royalblue", "goldenrod", "lightseagreen", "lightskyblue", "lightsalmon", "yellowgreen", "crimson", "mediumorchid", "darkgreen"]
#              noeboeski, innazieleń,  turkusowy, różowy, pomarańczowy, zielony, czerwony, fioletowy, zółty
#              aliceblue, darkgreen, aquamarine, lightcoral, lightsalmon, chartreuse, indianred, lavender, gold
             ,animation_frame="date"
             ,labels={"federal_state": "Federal State", "no_csum": "Number of people diagnosed with Covid-19"}
            )
fig.update_yaxes(range=[0, 35000])


order = total_pop.groupby("federal_state").agg({"no_csum":"max"}).sort_values("no_csum").index.to_list()
fig.update_layout(xaxis={'categoryarray':order, 'type': 'category'},
                 title = {'text': 'Cumulated cases of Covid-19 by region', 'xanchor': "center", 'x':0.5})



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
    