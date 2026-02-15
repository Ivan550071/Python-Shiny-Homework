import pandas as pd
import plotly.express as px
from shiny import reactive #I do this because shiny express doesn't support reactive functions yet
from shiny.express import input, ui, render
from htmltools import HTML

@reactive.calc()
def co2_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(url, usecols=["country", "iso_code", "year", "co2"])

    df["co2"] = pd.to_numeric(df["co2"], errors="coerce")
    df.dropna(subset=["iso_code", "co2"], inplace=True)
    df = df[df["co2"] > 0]
    df = df[df["iso_code"].str.len() == 3]

    return df

ui.page_opts(title="CO₂ Dashboard", fillable=True)

with ui.navset_bar(title="Select your Analysis"):
    with ui.nav_panel("Country - Co2 Time Series"):
        with ui.layout_sidebar():
            with ui.sidebar(open="always"):
                    @render.ui
                    def country_dropdown():
                        df = co2_data()
                        countries = sorted(df["country"].unique())
                        return ui.input_select("country", "Choose a Country:", choices=countries, selected="Austria"), ui.input_slider("years", "Rolling Mean (years)", 1, 20, 5)
            @render.ui
            def time_series_plot():
                df = co2_data()
                selected_country = input.country()
                window = input.years()

                df_country = df[df["country"] == selected_country].sort_values("year")
                df_country["smoothed"] = df_country["co2"].rolling(window=window, min_periods=1).mean()

                fig = px.line(df_country, x="year", y="co2", labels={"co2": "CO₂ emissions"},
                            title=f"CO₂ Emissions in {selected_country}", color_discrete_sequence=["#1f77b4"])
                fig.add_scatter(x=df_country["year"], y=df_country["smoothed"],
                                mode="lines", name=f"{window}-year Rolling Mean", line=dict(color="orange"))
                fig.update_layout(hovermode="x unified", margin=dict(t=40))

                return HTML(fig.to_html(include_plotlyjs="cdn", div_id="time_series_plot"))

    with ui.nav_panel("World Map - CO2 Emissions per Country"):
        with ui.layout_sidebar():
            with ui.sidebar(open="always"):
                    @render.ui
                    def year_slider():
                        df = co2_data()
                        years = df["year"]
                        return ui.input_slider("year", "Select Year", int(years.min()), int(years.max()), int(years.min()))
            @render.ui
            def world_map_plot():
                df = co2_data()
                selected_year = input.year()
                df_year = df[df["year"] == selected_year]

                fig = px.choropleth(
                    df_year,
                    locations="iso_code",
                    color="co2",
                    hover_name="country",
                    color_continuous_scale="Reds",
                    title=f"CO₂ Emissions in {selected_year}",
                )
                fig.update_layout(margin=dict(t=40))
                return HTML(fig.to_html(include_plotlyjs="cdn", div_id="world_map_plot"))