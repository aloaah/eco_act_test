import os
from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
base_path_main = os.path.dirname(os.path.abspath(__file__))
# Charger les données
data = pd.read_csv(os.path.join(base_path_main, "..", "data", "cleaned_data_dev_python.csv",)) 

# Préparer l'application Dash
app = Dash(__name__)

columns_to_display = ["nom_base_français", "unite_français", "sous-localisation_geographique_français", "type_poste", "nom_poste_français", "incertitude", "total_poste_non_decompose", "co2f", "ch4f", "ch4b", "n2o", "autres_ges", "co2b", "divers", "sf6"]
# Options uniques pour les filtres
unique_name = data["nom_base_français"].unique()
unique_types = data["type_ligne"].unique()

# Layout de l'application
app.layout = html.Div([
    html.H1("Visualisation des données d'émission", style={"textAlign": "center"}),

    html.Div([
        html.Label("Sélectionner un type d'élément:"),
        dcc.Dropdown(
            id="name-dropdown",
            options=[{"label": str(el), "value": el} for el in unique_name],
            value=unique_name[0],
            clearable=False
        )
    ]),

    html.Div([
        html.Label("Sélectionner une Unité:"),
        dcc.Dropdown(
            id="unit-dropdown",
            clearable=True
        )
    ]),

    html.Div(
        [
            html.Label("Raw data:"),
            dash_table.DataTable(id="main-dt", data=data.to_dict('records'), page_size=6),
        ]
    ),

    dcc.Graph(id="emissions-graph"),
])

@app.callback(
        Output("unit-dropdown", "options"), [Input("name-dropdown", "value")]
)
def element_options(name):
    return data.loc[data["nom_base_français"] == name, "unite_français"].unique()

@app.callback(
        Output("main-dt", "data"), [Input("name-dropdown", "value"), Input("unit-dropdown", "value")]
)
def get_table_data(name, unit):
    if unit is None:
        return data.loc[data["nom_base_français"] == name, columns_to_display].to_dict('records')
    else:
        return  data.loc[(data["nom_base_français"] == name) & (data["unite_français"] == unit), columns_to_display].to_dict('records')

# Callback pour mettre à jour le graphique
@app.callback(
    Output("emissions-graph", "figure"),
    [Input("name-dropdown", "value"),
     Input("unit-dropdown", "value")]
)
def update_graph(name, unit):
    gaz_columns = ["co2f", "ch4f", "ch4b", "n2o", "autres_ges", "co2b", "divers", "sf6"]


    filtered_data = data[
        (data["nom_base_français"] == name) &
        (data["unite_français"] == unit)
    ]


    gaz_columns = ["co2f", "ch4f", "ch4b", "n2o", "autres_ges", "co2b", "divers", "sf6"]
    hover_columns = ["commentaire_français", "type_poste", "nom_poste_français"]
    plot_data = filtered_data[["identifiant_de_lelement"] + gaz_columns + hover_columns].copy()
    # Melt the dataframe to a long format suitable for plotting with plotly
    melted_data = plot_data.melt(
        id_vars=["identifiant_de_lelement"] + hover_columns,
        value_vars=gaz_columns,
        var_name="Gaz",
        value_name="Valeur"
    )
    melted_data = melted_data.fillna({"type_poste": "global"})
    melted_data["index_col"] = melted_data["identifiant_de_lelement"].astype(str) + "_" + melted_data["type_poste"]
    print(melted_data)
    # Create a bar chart
    fig = px.bar(
        melted_data,
        x="index_col",
        y="Valeur",
        color="Gaz",
        hover_data=hover_columns, 
        labels={"identifiant_de_lelement": "Identifiant de l'élément", "Valeur": f"Émissions {unit}", "Gaz": "Type de gaz"},
        title="Émissions par type de gaz pour un élément",
        barmode="stack"
    )

    
    return fig

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)