import os
from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

base_path_main = os.path.dirname(os.path.abspath(__file__))
data = pd.read_excel(
    os.path.join(
        base_path_main,
        "..",
        "data",
        "donnees_candidats_dev_python.xlsx",
    )
)

app = Dash(__name__)

columns_to_display = [
    "Nom base français",
    "Unité français",
    "Sous-localisation géographique français",
    "Type poste",
    "Nom poste français",
    "Incertitude",
    "Total poste non décomposé",
    "CO2f",
    "CH4f",
    "CH4b",
    "N2O",
    "Autres GES",
    "CO2b",
]
unique_name = data["Nom base français"].unique()

app.layout = html.Div(
    [
        html.H1("Visualisation des données d'émission", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("Sélectionner un type d'élément:"),
                dcc.Dropdown(
                    id="name-dropdown",
                    options=[{"label": str(el), "value": el} for el in unique_name],
                    value=unique_name[0],
                    clearable=False,
                ),
            ]
        ),
        html.Div(
            [
                html.Label("Sélectionner une Unité:"),
                dcc.Dropdown(id="unit-dropdown", clearable=True),
            ]
        ),
        html.Div(
            [
                html.Label("Raw data:"),
                dash_table.DataTable(
                    id="main-dt", data=data.to_dict("records"), page_size=6
                ),
            ]
        ),
        dcc.Graph(id="emissions-graph"),
    ]
)


@app.callback(Output("unit-dropdown", "options"), [Input("name-dropdown", "value")])
def element_options(name):
    return data.loc[data["Nom base français"] == name, "Unité français"].unique()


@app.callback(
    Output("main-dt", "data"),
    [Input("name-dropdown", "value"), Input("unit-dropdown", "value")],
)
def get_table_data(name, unit):
    if unit is None:
        return data.loc[data["Nom base français"] == name, columns_to_display].to_dict(
            "records"
        )
    else:
        return data.loc[
            (data["Nom base français"] == name) & (data["Unité français"] == unit),
            columns_to_display,
        ].to_dict("records")


@app.callback(
    Output("emissions-graph", "figure"),
    [Input("name-dropdown", "value"), Input("unit-dropdown", "value")],
)
def update_graph(name, unit):

    filtered_data = data[
        (data["Nom base français"] == name) & (data["Unité français"] == unit)
    ]

    gaz_columns = ["CO2f", "CH4f", "CH4b", "N2O", "Autres GES", "CO2b"]
    hover_columns = ["Commentaire français", "Type poste", "Nom poste français"]

    plot_data = filtered_data[
        ["Identifiant de l'élément"] + gaz_columns + hover_columns
    ].copy()
    melted_data = plot_data.melt(
        id_vars=["Identifiant de l'élément"] + hover_columns,
        value_vars=gaz_columns,
        var_name="Gaz",
        value_name="Valeur",
    )
    melted_data = melted_data.fillna({"Type poste": "global"})
    melted_data["index_col"] = (
        melted_data["Identifiant de l'élément"].astype(str)
        + "_"
        + melted_data["Type poste"]
    )

    fig = px.bar(
        melted_data,
        x="index_col",
        y="Valeur",
        color="Gaz",
        hover_data=hover_columns,
        labels={
            "Identifiant de l'élément": "Identifiant de l'élément",
            "Valeur": f"Émissions {unit}",
            "Gaz": "Type de gaz",
            "index_col": "id élement_type poste",
        },
        title="Émissions par type de gaz pour un élément",
        barmode="stack",
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
