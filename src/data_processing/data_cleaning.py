import pandas as pd

def load_data(path : str="../data/donnees_candidats_dev_python.xlsx") -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Sheet1")

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.dropna(how="all", axis=1) 

    df.columns = [col.replace(" ", "_").replace("'", "").replace("é", "e").lower() for col in df.columns] #simplify column name
    
    df.fillna({"code_gaz_supplementaire_1" : '', "valeur_gaz_supplementaire_1": 0}, inplace=True) #pivot on code_gaz_supplementaire_1, valeur_gaz_supplementaire_1 
    additional_gases = df.pivot(columns='code_gaz_supplementaire_1', values='valeur_gaz_supplementaire_1')
    additional_gases.drop([""], axis=1, inplace=True)
    additional_gases.columns = [col.lower() for col in additional_gases.columns]
    df = df.join(additional_gases)
    df.drop(columns=['code_gaz_supplementaire_1', 'valeur_gaz_supplementaire_1'], inplace=True)
    
    df["code_de_la_categorie"] = df["code_de_la_categorie"].replace(" > ", "/", regex=True) #simplify syntax
    
    return df