# %%
import plotly.graph_objects as go
import pandas as pd
import sys


def normalize(df):
    initial_open = df.iloc[0].Open
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].divide(initial_open)
    return df


dax_data = normalize(pd.read_csv("../data/^dax_d.csv"))
shc_data = normalize(pd.read_csv("../data/^shc_d.csv"))
spx_data = normalize(pd.read_csv("../data/^spx_d.csv"))


fig = go.Figure(data=[go.Candlestick(name='DAX', x=dax_data['Date'],
                                     open=dax_data['Open'], high=dax_data['High'],
                                     low=dax_data['Low'], close=dax_data['Close']),

                      go.Candlestick(name='SSE Composite', x=shc_data['Date'],
                                     increasing_line_color='cyan', decreasing_line_color='gray',
                                     open=shc_data['Open'], high=shc_data['High'],
                                     low=shc_data['Low'], close=shc_data['Close']),

                      go.Candlestick(name='S&P 500', x=spx_data['Date'],
                                     increasing_line_color='blue', decreasing_line_color='magenta',
                                     open=spx_data['Open'], high=spx_data['High'],
                                     low=spx_data['Low'], close=spx_data['Close'])
                      ])

fig.update_layout(title={'text': 'Covid impact on stock market', 'xanchor': "center", 'x': 0.5})

# fig.update_layout(
#     title='The Great Recession',
#     yaxis_title='AAPL Stock',
#     shapes=[dict(
#         x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
#         line_width=2)],
#     annotations=[dict(
#         x='2016-12-09', y=0.05, xref='x', yref='paper',
#         showarrow=False, xanchor='left', text='Increase Period Begins')]
# )
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

# %%
