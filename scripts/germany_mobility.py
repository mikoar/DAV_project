import plotly
import plotly.graph_objs as go
import pandas as pd
import sys

mobility_germany = pd.read_csv("../data/mobility_germany.csv")

mobility_germany = mobility_germany.loc[mobility_germany.sub_region_1.isnull(), :]

colors = (['indianred']*2+['lightsalmon']*5)*12 + ['indianred']

fig = go.Figure()

fig.add_traces(go.Bar(
    x=mobility_germany.date,
    y=mobility_germany.retail_and_recreation_percent_change_from_baseline,
    hovertemplate= "Date: %{x}<br>" + \
                    "% change in mobility: %{y}<br>" + \
                    "<extra></extra>",
    marker_color=colors 
))

fig.add_traces(go.Bar(
    x=mobility_germany.date,
    y=mobility_germany.grocery_and_pharmacy_percent_change_from_baseline,
    hovertemplate= "Date: %{x}<br>" + \
                    "% change in mobility: %{y}<br>" + \
                    "<extra></extra>",
    visible = False,
    marker_color=colors 
))

fig.add_traces(go.Bar(
    x=mobility_germany.date,
    y=mobility_germany.parks_percent_change_from_baseline,
    hovertemplate= "Date: %{x}<br>" + \
                    "% change in mobility: %{y}<br>" + \
                    "<extra></extra>",
    visible = False,
    marker_color=colors 
))


fig.add_traces(go.Bar(
    x=mobility_germany.date,
    y=mobility_germany.transit_stations_percent_change_from_baseline,
    hovertemplate= "Date: %{x}<br>" + \
                    "% change in mobility: %{y}<br>" + \
                    "<extra></extra>",
    visible = False,
    marker_color=colors 
))

fig.add_traces(go.Bar(
    x=mobility_germany.date,
    y=mobility_germany.workplaces_percent_change_from_baseline,
    hovertemplate= "Date: %{x}<br>" + \
                    "% change in mobility: %{y}<br>" + \
                    "<extra></extra>",
    visible = False,
    marker_color=colors 
))

fig.add_traces(go.Bar(
    x=mobility_germany.date,
    y=mobility_germany.residential_percent_change_from_baseline,
    hovertemplate= "Date: %{x}<br>" + \
                    "% change in mobility: %{y}<br>" + \
                    "<extra></extra>",
    visible = False,
    marker_color=colors 
))

updatemenus = list([
    dict(active=1,
         yanchor="top",
         x=0.13,
         y=1.05,
         buttons=list([
            dict(label='Retail & Recreation',
                 method='update',
                 args=[{'visible': [True, False, False, False, False, False]},
                       {'title': 'Retail & Recreation Mobility Change From Baseline'}]),
            dict(label='Grocery & Pharmacy',
                 method='update',
                 args=[{'visible': [False, True, False, False, False, False]},
                       {'title': 'Grocery & Pharmacy Mobility Change From Baseline'}]),
             dict(label='Parks',
                 method='update',
                 args=[{'visible': [False, False, True, False, False, False]},
                       {'title': 'Parks Mobility Change From Baseline'}]),
             dict(label='Transit Stations',
                 method='update',
                 args=[{'visible': [False, False, False, True, False, False]},
                       {'title': 'Transit Stations Mobility Change From Baseline'}]),
             dict(label='Workplaces',
                 method='update',
                 args=[{'visible': [False, False, False, False, True, False]},
                       {'title': 'Workplaces Mobility Change From Baseline'}]),
             dict(label='Residential',
                 method='update',
                 args=[{'visible': [False, False, False, False, False, True]},
                       {'title': 'Residential Mobility Change From Baseline'}]),
            ]),
        )
    ])

fig.update_layout(
    updatemenus = updatemenus,
    title={
        'text': "Mobility report",
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