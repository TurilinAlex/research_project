import os

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Output, Input, State, dcc, html, callback
from plotly.graph_objs import Scatter
from pydantic import BaseModel

from trading_algorithm import UnionExtremes


class Config(BaseModel):
    eps: list[int]
    repeat: list[int]
    trend_eps: int
    split: int


config = Config.parse_file("config.json")
coincident = config.repeat
start_eps = config.eps
trend_eps = config.trend_eps
split = config.split
offset = 0.001


def create_vertical_line(x_position, id_, color):
    return {
        "type": "line",
        "x0": x_position,
        "x1": x_position,
        "y0": 0,
        "y1": 1,
        "yref": "paper",
        "line": {
            "color": color,
            "width": 1,
        },
        "name": f"vline_{id_}",
    }


def prepare_date():
    start_date = pd.Timestamp(df["Date"][0])
    end_date = start_date + pd.Timedelta(minutes=1 * len(df))

    # Создаем равномерный ряд дат с шагом в 1 минуту
    _date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq="1min",
        inclusive="left",
    )
    df["Date"] = _date_range

    return _date_range


def calk_extr(data):
    ext = UnionExtremes(values=data)
    for c, e in zip(coincident, start_eps):
        ext.extract_extremes(coincident=c, start_eps=e)

    ext.extract_trends(eps=trend_eps)

    return ext


def plot_min_extr(shift, ext):
    for i in range(1, len(coincident) + 1):
        eps = ext.get_extr_eps_min(after_iter=i)
        x = date_range[ext.get_extr_indexes_min(after_iter=i) + shift]
        y = ext.get_extr_values_min(after_iter=i)
        y_max = min(y)
        y = y - (y_max * i * offset)
        fig.add_scatter(
            x=x,
            y=y,
            mode="markers",
            marker={
                "symbol": "arrow-up-open",
                "size": 5 * i,
                "line": {"width": i},
                "color": "#404040",
            },
            hovertemplate="<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
            + f"Extr eps: {eps}<extra></extra>",
            name=f"Extremum Min {i}",
        )


def plot_min_trend(shift, ext, after_iter):
    x = date_range[ext.get_trends_indexes_min(after_iter=after_iter) + shift]
    y = ext.get_trends_values_min(after_iter=after_iter)
    y_max = min(y)
    y = y - (y_max * len(coincident) * offset)
    fig.add_scatter(
        x=x,
        y=y,
        mode="markers",
        marker={
            "symbol": "arrow-bar-up-open",
            "size": 5 * after_iter,
            "line": {"width": after_iter},
            "color": "#404040",
        },
        hovertemplate="<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
        + f"Trend eps: {config.trend_eps}<extra></extra>",
        name=f"Trend Min {after_iter}",
    )


def update_plot_min_extr(shift, ext):
    for i in range(1, len(coincident) + 1):
        eps = ext.get_extr_eps_min(after_iter=i)
        x = date_range[ext.get_extr_indexes_min(after_iter=i) + shift]
        y = ext.get_extr_values_min(after_iter=i)
        y_max = min(y)
        y = y - (y_max * i * offset)
        fig.update_traces(
            {
                "x": x,
                "y": y,
                "hovertemplate": "<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
                + f"Extr eps: {eps}<extra></extra>",
            },
            selector={"name": f"Extremum Min {i}"},
        )


def update_plot_min_trend(shift, ext, after_iter):
    x = date_range[ext.get_trends_indexes_min(after_iter=after_iter) + shift]
    y = ext.get_trends_values_min(after_iter=after_iter)
    y_max = min(y)
    y = y - (y_max * len(coincident) * offset)
    fig.update_traces(
        {
            "x": x,
            "y": y,
            "hovertemplate": "<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
            + f"Trend eps: {config.trend_eps}<extra></extra>",
        },
        selector={"name": f"Trend Min {after_iter}"},
    )


def plot_max_extr(shift, ext):
    for i in range(1, len(coincident) + 1):
        eps = ext.get_extr_eps_max(after_iter=i)
        x = date_range[ext.get_extr_indexes_max(after_iter=i) + shift]
        y = ext.get_extr_values_max(after_iter=i)
        y_max = max(y)
        y = y + (y_max * i * offset)
        fig.add_scatter(
            x=x,
            y=y,
            mode="markers",
            marker={
                "symbol": "arrow-down-open",
                "size": 5 * i,
                "line": {"width": i},
                "color": "#404040",
            },
            hovertemplate="<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
            + f"Extr eps: {eps}<extra></extra>",
            name=f"Extremum Max {i}",
        )


def plot_max_trend(shift, ext, after_iter):
    x = date_range[ext.get_trends_indexes_max(after_iter=after_iter) + shift]
    y = ext.get_trends_values_max(after_iter=after_iter)
    y_max = max(y)
    y = y + (y_max * len(coincident) * offset)
    fig.add_scatter(
        x=x,
        y=y,
        mode="markers",
        marker={
            "symbol": "arrow-bar-down-open",
            "size": 5 * after_iter,
            "line": {"width": after_iter},
            "color": "#404040",
        },
        hovertemplate="<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
        + f"Trend eps: {config.trend_eps}<extra></extra>",
        name=f"Trend Max {after_iter}",
    )


def update_plot_max_extr(shift, ext):
    for i in range(1, len(coincident) + 1):
        eps = ext.get_extr_eps_max(after_iter=i)
        x = date_range[ext.get_extr_indexes_max(after_iter=i) + shift]
        y = ext.get_extr_values_max(after_iter=i)
        y_max = max(y)
        y = y + (y_max * i * offset)
        fig.update_traces(
            {
                "x": x,
                "y": y,
                "hovertemplate": "<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
                + f"Extr eps: {eps}<extra></extra>",
            },
            selector={"name": f"Extremum Max {i}"},
        )


def update_plot_max_trend(shift, ext, after_iter):
    x = date_range[ext.get_trends_indexes_max(after_iter=after_iter) + shift]
    y = ext.get_trends_values_max(after_iter=after_iter)
    y_max = max(y)
    y = y + (y_max * len(coincident) * offset)
    fig.update_traces(
        {
            "x": x,
            "y": y,
            "hovertemplate": "<i>%{x|%d-%m-%Y %H:%M}</i> <br>%{y}</br>"
            + f"Trend eps: {config.trend_eps}<extra></extra>",
        },
        selector={"name": f"Trend Max {after_iter}"},
    )


app = Dash(__name__)
fig = go.Figure()
fig.update_layout(legend_orientation="h")
fig.update_layout(
    legend={"x": 0.5, "xanchor": "center", "yanchor": "bottom", "y": -0.1}
)
fig.update_layout(margin={"l": 0, "r": 20, "t": 0, "b": 100})
fig.update_layout(
    yaxis_title="y Axis Title",
)
fig.update_layout(xaxis_rangeslider_visible=False)

df = pd.read_csv(
    "/Users/aleksandrturilin/HomeProject/graduate-school/core/__run"
    "/experiment_1/AUD_CAD/2001-11-28 04:10:00_2001-12-27 04:09:00/input.csv"
)
date_range = prepare_date()
dates_list = date_range.strftime("%d-%m-%Y %H:%M").tolist()

# Задание интервала по оси x
x_start = date_range[0]
x_end = date_range[-1]
fig.update_layout(xaxis=dict(range=[x_start, x_end]))

# Define the directory path
directory = "assets"

# Check if the directory exists, if not, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Now, open the file for writing
with open(os.path.join(directory, "tooltip.js"), "w") as file:
    file.write(
        f"let datesArray = {dates_list}\n"
        + """
        window.dccFunctions = window.dccFunctions || {};
        window.dccFunctions.datetime = function (value) {
            return datesArray[value];
        }
        """
    )


fig.add_candlestick(
    x=df["Date"],
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    increasing={
        "line": {
            "width": 1,
            "color": "#404040",
        },
        "fillcolor": "#FFFFFF",
    },
    decreasing={
        "line": {
            "width": 1,
            "color": "#404040",
        },
        "fillcolor": "#404040",
    },
    name="",
)

values = df["Close"].values


def main():
    print("Start")
    x_pos_range = [0, config.split]
    fig.add_shape(create_vertical_line(date_range[x_pos_range[0]], 0, "Red"))
    fig.add_shape(create_vertical_line(date_range[x_pos_range[1]], 1, "Green"))

    app.layout = html.Div(
        [
            html.Button(
                "Recalculate",
                id="button",
                style={
                    "marginLeft": 60,
                    "marginBottom": 3,
                    "width": "95.5%",
                    "height": "2vh",
                },
            ),
            dcc.Loading(
                [
                    dcc.Graph(
                        id="graph",
                        figure=fig,
                        style={
                            "width": "100%",
                            "height": "93vh",
                        },
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.RangeSlider(
                        id="range-slider",
                        min=0,
                        max=len(df),
                        step=5,
                        value=x_pos_range,
                        marks=None,
                        pushable=2000,
                        allowCross=False,
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True,
                            "style": {
                                "color": "LightSteelBlue",
                                "fontSize": "14px",
                            },
                            "template": "{value}",
                            "transform": "datetime",
                        },
                    )
                ],
                style={
                    "marginLeft": 37,
                    "marginRight": 0,
                    "height": "5vh",
                },
            ),
        ],
        style={"width": "100%", "height": "100vh", "margin": "0"},
    )

    @callback(
        Output("graph", "figure"),
        Input("button", "n_clicks"),
        State("range-slider", "value"),
    )
    def update_graph(n_clicks, range_value):

        fig.update_shapes(
            {
                "x0": date_range[range_value[0]],
                "x1": date_range[range_value[0]],
            },
            selector={
                "name": "vline_0",
            },
        )
        fig.update_shapes(
            {
                "x0": date_range[range_value[1]],
                "x1": date_range[range_value[1]],
            },
            selector={
                "name": "vline_1",
            },
        )

        # fmt: off
        extr = calk_extr(values[range_value[0]: range_value[1]])
        # fmt: on

        if not n_clicks:
            fig.data = [trace for trace in fig.data if not isinstance(trace, Scatter)]

            plot_min_extr(range_value[0], extr)
            plot_min_trend(range_value[0], extr, len(coincident))

            plot_max_extr(range_value[0], extr)
            plot_max_trend(range_value[0], extr, len(coincident))

            return fig

        update_plot_min_extr(range_value[0], extr)
        update_plot_min_trend(range_value[0], extr, len(coincident))

        update_plot_max_extr(range_value[0], extr)
        update_plot_max_trend(range_value[0], extr, len(coincident))

        return fig

    app.run_server(debug=False)


if __name__ == "__main__":
    main()
