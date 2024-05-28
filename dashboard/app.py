from ipyleaflet import Marker, DivIcon, Map, basemaps, leaflet, Popup
from shiny import App, reactive, ui
from shinywidgets import output_widget, render_widget
import pandas as pd
import shiny.experimental as x
import plotly.express as px
import plotly.graph_objects as go
from plotly_streaming import render_plotly_streaming
from pathlib import Path
import faicons

category_colors = {
    "Serverless": 0,
    "Containers": 1,
    "Cloud Operations": 2,
    "Security & Identity": 3,
    "Dev Tools": 4,
    "Machine Learning & GenAI": 5,
    "Data": 6,
    "Networking & Content Delivery": 7,
    "Front-End Web & Mobile": 8,
    "Storage": 9,
    "Game Tech": 10,
}


def read_data():
    df = pd.read_csv(
        Path(__file__).parent / "data/anonymized_cb_data.csv", delimiter=";"
    )
    df["cohort"] = df["cohort"].astype(str)
    return df


def get_color_theme(theme, list_categories=None):

    if theme == "Custom":
        list_colors = [
            "#F6AA54",
            "#2A5D78",
            "#9FDEF1",
            "#B9E52F",
            "#E436BB",
            "#6197E2",
            "#863CFF",
            "#30CB71",
            "#ED90C7",
            "#DE3B00",
            "#25F1AA",
            "#C2C4E3",
            "#33AEB1",
            "#8B5011",
            "#A8577B",
        ]
    elif theme == "RdBu":
        list_colors = px.colors.sequential.RdBu.copy()
        del list_colors[5]  # Remove color position 5
    elif theme == "GnBu":
        list_colors = px.colors.sequential.GnBu
    elif theme == "RdPu":
        list_colors = px.colors.sequential.RdPu
    elif theme == "Oranges":
        list_colors = px.colors.sequential.Oranges
    elif theme == "Blues":
        list_colors = px.colors.sequential.Blues
    elif theme == "Reds":
        list_colors = px.colors.sequential.Reds
    elif theme == "Hot":
        list_colors = px.colors.sequential.Hot
    elif theme == "Jet":
        list_colors = px.colors.sequential.Jet
    elif theme == "Rainbow":
        list_colors = px.colors.sequential.Rainbow

    if list_categories is not None:
        final_list_colors = [
            list_colors[category_colors[category] % len(list_colors)]
            for category in list_categories
        ]
    else:
        final_list_colors = list_colors

    return final_list_colors


def get_color_template(mode):
    if mode == "light":
        return "plotly_white"
    else:
        return "plotly_dark"


def get_background_color_plotly(mode):
    if mode == "light":
        return "white"
    else:
        return "rgb(29, 32, 33)"


def get_map_theme(mode):
    print(mode)
    if mode == "light":
        return basemaps.CartoDB.Positron
    else:
        return basemaps.CartoDB.DarkMatter


def create_custom_icon(count):

    size_circle = 45 + (count / 10)

    # Define the HTML code for the icon
    html_code = f"""
    <div style=".leaflet-div-icon.background:transparent !important;
        position:relative; width: {size_circle}px; height: {size_circle}px;">
        <svg width="{size_circle}" height="{size_circle}" viewBox="0 0 42 42"
            class="donut" aria-labelledby="donut-title donut-desc" role="img">
            <circle class="donut-hole" cx="21" cy="21" r="15.91549430918954"
                fill="white" role="presentation"></circle>
            <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954"
                fill="transparent" stroke="color(display-p3 0.9451 0.6196 0.2196)"
                stroke-width="3" role="presentation"></circle>
            <text x="50%" y="60%" text-anchor="middle" font-size="13"
                font-weight="bold" fill="#000">{count}</text>
        </svg>
    </div>
    """

    # Create a custom DivIcon
    return DivIcon(
        icon_size=(50, 50), icon_anchor=(25, 25), html=html_code, class_name="dummy"
    )


def create_custom_popup(country, total, dark_mode, color_theme):

    # Group by 'region' and count occurrences of each region
    df = read_data()
    category_counts = (
        df[df.country == country].groupby("category").size().reset_index(name="count")
    )

    # Create a pie chart using plotly.graph_objects
    data = [
        go.Pie(
            labels=category_counts["category"],
            values=category_counts["count"],
            hole=0.3,
            textinfo="percent+label",
            marker=dict(
                colors=get_color_theme(color_theme, category_counts["category"])
            ),
        )
    ]

    # Set title and template
    layout = go.Layout(
        title=f"{total} Community Builders in {country}",
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color_plotly(dark_mode),
        title_x=0.5,
        titlefont=dict(size=20),
        showlegend=False,
    )

    figure = go.Figure(data=data, layout=layout)
    figure.update_traces(
        textposition="outside", textinfo="percent+label", textfont=dict(size=15)
    )
    figure.layout.width = 600
    figure.layout.height = 400

    popup = Popup(child=go.FigureWidget(figure), max_width=600, max_height=400)

    return popup


app_ui = ui.page_fillable(
    ui.page_navbar(
        ui.nav_panel(
            "Dashboard",
            ui.row(
                ui.layout_columns(
                    ui.value_box(
                        title="N° Community Builders",
                        showcase=faicons.icon_svg(
                            "people-group", width="50px", fill="#FD9902 !important"
                        ),
                        value=len(read_data()),
                    ),
                    ui.value_box(
                        title="N° Countries",
                        showcase=faicons.icon_svg(
                            "globe", width="50px", fill="#FD9902 !important"
                        ),
                        value=len(read_data().country.unique()),
                    ),
                    ui.value_box(
                        title="N° Categories",
                        showcase=faicons.icon_svg(
                            "list", width="50px", fill="#FD9902 !important"
                        ),
                        value=len(read_data().category.unique()),
                    ),
                    ui.value_box(
                        title="N° Cohorts",
                        showcase=faicons.icon_svg(
                            "calendar", width="50px", fill="#FD9902 !important"
                        ),
                        value=len(read_data().cohort.unique()),
                    ),
                    col_widths=(3, 3, 3, 3),
                ),
            ),
            ui.row(
                ui.layout_columns(
                    x.ui.card(output_widget("plot_0")),
                    x.ui.card(output_widget("plot_1")),
                    x.ui.card(output_widget("plot_2")),
                    col_widths=(4, 4, 4),
                ),
            ),
            ui.row(
                ui.layout_columns(
                    x.ui.card(output_widget("plot_3")),
                    x.ui.card(output_widget("plot_4")),
                    col_widths=(6, 6),
                ),
            ),
        ),
        ui.nav_panel(
            "Map",
            ui.row(
                ui.card(
                    output_widget("map_full"),
                    id="card_map",
                ),
            ),
        ),
        title=ui.img(src="images/logo.png", style="max-width:100px;width:100%"),
        id="page",
        sidebar=ui.sidebar(
            ui.input_select(
                id="color_theme",
                label="Color theme",
                choices=[
                    "Custom",
                    "RdBu",
                    "GnBu",
                    "RdPu",
                    "Oranges",
                    "Blues",
                    "Reds",
                    "Hot",
                    "Jet",
                    "Rainbow",
                ],
                selected="Custom",
            ),
            ui.input_dark_mode(id="dark_mode", mode="light"),
            open="closed",
        ),
        footer=ui.h6(
            "Made by Robert Garcia Ventura © 2024",
            style="color: white !important; text-align: center;",
        ),
        window_title="AWS Community Builders Dashboard",
    ),
    ui.tags.style(
        """
        .leaflet-popup-content {
            width: 600px !important;
        }
        .leaflet-div-icon {
            background: transparent !important;
            border: transparent !important;
        }
        .collapse-toggle {
            color: #FD9902 !important;
        }
        .main {
            /* Background image */
            background-image: url("images/background_dark_full.png");
            height: 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
        div#map_full.html-fill-container {
            height: -webkit-fill-available !important;
            min-height: 850px !important;
            max-height: 2000px !important;
        }
        div#main_panel.html-fill-container {
            height: -webkit-fill-available !important;
        }
        """
    ),
    icon="images/favicon.ico",
)


def server(input, output, session):

    df = read_data()

    df_countries = pd.read_csv(
        Path(__file__).parent / "data/countries.csv", delimiter=";"
    )

    @reactive.Calc
    @output
    @render_widget
    @reactive.event(input.dark_mode)
    def map_full():
        map = Map(
            basemap=get_map_theme(input.dark_mode()),
            center=(25.00, 20.00),
            zoom=3,
            scroll_wheel_zoom=True,
        )

        with ui.Progress(min=0, max=len(df_countries)) as progress:
            progress.set(
                message="Calculation in progress", detail="This may take a while..."
            )

            for index, row in df_countries.iterrows():
                lat = float(row["latitud"])
                lon = float(row["longitud"])
                country = row["country"]
                count = row["count"]

                # Add a marker with the custom icon to the map
                custom_icon = create_custom_icon(count)

                # Create custom Pie chart with Community Builders from each country
                custom_popup = create_custom_popup(
                    country, count, input.dark_mode(), input.color_theme()
                )

                marker = Marker(
                    location=(lat, lon),
                    icon=custom_icon,
                    draggable=False,
                    popup=custom_popup,
                )

                map.add_layer(marker)

                progress.set(index, message=f"Calculating country {country}")

            map.add_control(leaflet.ScaleControl(position="bottomleft"))

            progress.set(index, message="Rendering the map...")

        return map

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_tmp():

        df_countries = (
            df.groupby("country")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)[:10]
        )

        df_other_countries = pd.DataFrame(
            [
                [
                    "Others",
                    df.groupby("country")
                    .size()
                    .reset_index(name="count")
                    .sort_values("count", ascending=False)[10:]["count"]
                    .sum(),
                ]
            ],
            columns=["country", "count"],
        )
        df_countries = pd.concat([df_countries, df_other_countries])

        # Plot 0: Bar Chart of Community Builders by Category
        fig0 = px.pie(
            df_countries,
            names="country",
            values="count",
            hole=0.3,
            labels={"country": "Country", "count": "Number of Community Builders"},
            title="Community Builders by Country",
            template=get_color_template(input.dark_mode()),
            color_discrete_sequence=get_color_theme(input.color_theme()),
        )

        fig0.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig0.update_traces(
            textposition="outside", textinfo="percent+label", textfont=dict(size=15)
        )
        fig0.update_layout(showlegend=False)

        return fig0

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_0():

        # Plot 0: Bar Chart of Community Builders by Category
        fig0 = px.pie(
            df.groupby("region").size().reset_index(name="count"),
            names="region",
            values="count",
            hole=0.3,
            labels={"region": "Region", "count": "Number of Community Builders"},
            title="Community Builders by Region",
            template=get_color_template(input.dark_mode()),
            color_discrete_sequence=get_color_theme(input.color_theme()),
        )

        fig0.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig0.update_traces(
            textposition="outside", textinfo="percent+label", textfont=dict(size=15)
        )
        fig0.update_layout(showlegend=False)

        return fig0

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_2():

        fig1 = px.pie(
            df.groupby("cohort").size().reset_index(name="count"),
            names="cohort",
            values="count",
            hole=0.3,
            labels={"cohort": "Cohort", "count": "Number of Community Builders"},
            title="Community Builders by Cohort",
            template=get_color_template(input.dark_mode()),
            color_discrete_sequence=get_color_theme(input.color_theme()),
        )

        fig1.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig1.update_traces(
            textposition="outside", textinfo="percent+label", textfont=dict(size=15)
        )
        fig1.update_layout(showlegend=False)

        return fig1

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_1():

        df_categories = (
            df.groupby("category")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
        )
        fig2 = px.pie(
            df_categories,
            names="category",
            values="count",
            hole=0.3,
            labels={"category": "Category", "count": "Number of Community Builders"},
            title="Community Builders by Category",
            template=get_color_template(input.dark_mode()),
            color_discrete_sequence=get_color_theme(
                input.color_theme(), df_categories.category
            ),
        )

        fig2.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig2.update_traces(
            textposition="outside", textinfo="percent+label", textfont=dict(size=15)
        )
        fig2.update_layout(showlegend=False)

        return fig2

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_4():

        df_counts = (
            df[["cohort", "category"]]
            .value_counts()
            .reset_index(name="count")
            .sort_values(by=["cohort", "category"])
        )
        total_cohort = (
            df[["cohort"]]
            .value_counts()
            .reset_index(name="count")
            .sort_values(by="cohort")
        )

        # Create the bar plot
        fig3 = px.bar(
            df_counts,
            x="cohort",
            y="count",
            color="category",
            text="count",
            text_auto=True,
            labels={
                "cohort": "Cohort",
                "count": "Number of Community Builders",
                "category": "Category",
            },
            title="N° Community Builders by Cohort and Category",
            template=get_color_template(input.dark_mode()),
            color_discrete_sequence=get_color_theme(
                input.color_theme(), df_counts.category
            ),
            category_orders={
                "cohort": ["2020 beta", "2020", "2021", "2022", "2023", "2024"]
            },
        )

        fig3.update_traces(textposition="inside")

        fig3.add_trace(
            go.Scatter(
                x=total_cohort["cohort"],
                y=total_cohort["count"],
                text=total_cohort["count"],
                mode="text",
                textposition="top center",
                textfont=dict(
                    size=15,
                ),
                showlegend=False,
            )
        )

        fig3.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig3.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
        fig3.update_yaxes(range=[0, max(total_cohort["count"]) + 100])
        return fig3

    @reactive.Calc
    @output
    @render_plotly_streaming()
    def plot_3():

        top_10_countries = (
            df.groupby(["country"])
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)[:10]
        )
        list_top_10_countries = top_10_countries["country"].values
        country_index = {
            country: index for index, country in enumerate(list_top_10_countries)
        }
        df["country_index"] = df["country"].map(country_index)
        df_top_10_countries = (
            df[[row in list_top_10_countries for row in df.country]]
            .groupby(["country", "country_index", "cohort"])
            .size()
            .reset_index(name="count")
            .sort_values("country_index")
        )

        fig4 = px.bar(
            df_top_10_countries,
            x="country",
            y="count",
            color="cohort",
            text="count",
            labels={
                "country": "Country",
                "count": "Number of Community Builders",
                "cohort": "Cohort",
            },
            title="Top 10 countries with more Community Builders by Cohort",
            template=get_color_template(input.dark_mode()),
            color_discrete_sequence=get_color_theme(input.color_theme()),
            category_orders={
                "cohort": ["2024", "2023", "2022", "2021", "2020", "2020 beta"]
            },
        )
        fig4.update_traces(textposition="inside")

        fig4.add_trace(
            go.Scatter(
                x=top_10_countries["country"],
                y=top_10_countries["count"],
                text=top_10_countries["count"],
                mode="text",
                textposition="top center",
                textfont=dict(size=15),
                showlegend=False,
            )
        )

        fig4.update_layout(
            paper_bgcolor=get_background_color_plotly(input.dark_mode()), title_x=0.5
        )
        fig4.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
        fig4.update_yaxes(range=[0, max(top_10_countries["count"]) + 40])
        return fig4


static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)
