# a4_ex1/app.py
import pandas as pd
from io import BytesIO
from shiny.express import input, ui, render, session
from shiny import reactive
import plotly.express as px

ui.page_opts(title="Data Cleaner", fillable=True)

with ui.sidebar():
        ui.input_file("file", "Upload CSV File"),
        ui.input_action_button("analyze", "Analyze"),
        ui.input_selectize("drop_cols", "Drop Columns", choices=[], multiple=True),
        ui.input_select("missing", "With NaNs", 
                        choices=["No change", "Replace with 0", "Replace with column mean", 
                                 "Replace with column median", "Drop rows with missing values"],
                        selected="No change"),
        ui.input_selectize("transform_cols", "Columns to transform", choices=[], multiple=True),
        ui.input_select("transform", "Transform Strategy", 
                        choices=["None", "Normalize", "Standardize"], selected="None"),
        ui.input_action_button("clean", "Clean"),
        @render.download(label="Download Cleaed Data")
        def download():
            df = reactive_values["current"]
            
            if df is None or df.empty:
                ui.notification_show("No data available to download.", duration=3)
                return

            output = BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)

            return output.getvalue(), "cleaned_data.csv"
        ui.input_action_button("reset", "Reset"),
        ui.input_dark_mode(id="mode")

reactive_values = {
    "original": None,
    "current": None
}

with ui.navset_pill(id="navtabs"):
    with ui.nav_panel("Data"):
        ""
    with ui.nav_panel("Analysis"):
        ""

#display df after clicking on navset
@render.data_frame
def display_table():
    selected_panel = input.navtabs()
    if reactive_values["current"] is None:
        return pd.DataFrame()

    df = reactive_values["current"]

    if selected_panel == "Data":
        return df
    elif selected_panel == "Analysis":
        summary = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str),
            "missing_values": df.isnull().sum(),
            "missing_percent": df.isnull().mean() * 100
        }).sort_values(by="missing_values", ascending=False)
        return summary
    
    return pd.DataFrame()

#here i check for file exceptions (not being csv)
@reactive.effect
@reactive.event(input.file)
def handle_file_upload():
    try:
        file = input.file()
        if file is None:
            return
        df = pd.read_csv(file[0]["datapath"])
        reactive_values["original"] = df.copy()
        reactive_values["current"] = df.copy()
        ui.update_selectize("drop_cols", choices=df.columns.tolist())
        num_cols = df.select_dtypes(include="number").columns.tolist()
        ui.update_selectize("transform_cols", choices=num_cols)
    except Exception as e:
        ui.notification_show(f"Error loading file: {e}", duration=5)


#func for cleaning the df depending on way of Replacement
@reactive.effect
@reactive.event(input.clean)
def _():
    df = reactive_values["current"]
    if df is None:
        ui.notification_show("No data loaded to clean.", duration=3)
        return

    to_drop = input.drop_cols()

    to_drop = [col[0] if isinstance(col, tuple) else col for col in to_drop] #flatten the columnn name because of bugs

    if to_drop:
        print("Attempting to drop:", to_drop)
        print("Actual columns in DataFrame:", df.columns)
        df = df.drop(columns=to_drop)

    method = input.missing()
    if method == "Replace with 0":
        df = df.fillna(0)
    elif method == "Replace with column mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif method == "Replace with column median":
        df = df.fillna(df.median(numeric_only=True))
    elif method == "Drop rows with missing values":
        df = df.dropna()

    transform = input.transform()
    cols = input.transform_cols()

    valid_transform_cols = [col for col in cols if col in df.columns] #again flattening

    if transform != "None" and valid_transform_cols:
        for col in valid_transform_cols:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                if transform == "Normalize":
                    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
                elif transform == "Standardize":
                    df[col] = (df[col] - df[col].mean()) / df[col].std()

    reactive_values["current"] = df
    ui.notification_show("Data cleaned successfully.", duration=3)


#func for the Reset button
@reactive.effect
@reactive.event(input.reset)
def _():
    if reactive_values["original"] is not None:
        reactive_values["current"] = reactive_values["original"].copy()
        ui.notification_show("Data has been reset to original.", duration=3)


#func for Dark/White mode implementation
@render.ui
def style():
    color = "gainsboro" if input.mode() == "light" else "black"
    css = f"{{ background: {color} }}"
    
    return ui.tags.style(css)