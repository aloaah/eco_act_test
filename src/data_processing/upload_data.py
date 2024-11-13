from src.database.db import SessionLocal
from src.database.models import EmissionData, QualityMetrics, ProcessType, Element
import pandas as pd

def process_emission_row(row, element_id, session):
    """
    Process a single row from the DataFrame and add the corresponding
    EmissionData, QualityMetrics, and ProcessType entries to the database.
    """
    # Create the `EmissionData` instance
    emission_data = EmissionData(
        element_id=element_id,
        total_poste_non_decompose=row.get('total_poste_non_decompose'),
        co2f=row.get('co2f'),
        ch4f=row.get('ch4f'),
        n2o=row.get('n2o'),
        autres_ges=row.get('autres_ges'),
        co2b=row.get('co2b'),
        unite_francais=row.get('unite_francais'),
        divers=row.get('divers'),  
        sf6=row.get('sf6'),
        incertitude=row.get("incertitude")
    )
    session.add(emission_data)
    session.flush()  # Assigns `emission_id` to `emission_data`

    # Check if QualityMetrics is not empty before creating it
    if any(row.get(metric) for metric in ['qualite_ter', 'qualite_gr', 'qualite_tir', 'qualite_c', 'qualite_p', 'qualite_m', "transparence", "qualite"]):
        quality_metrics = QualityMetrics(
            emission_id=emission_data.emission_id,
            qualite_ter=row.get('qualite_ter'),
            qualite_gr=row.get('qualite_gr'),
            qualite_tir=row.get('qualite_tir'),
            qualite_c=row.get('qualite_c'),
            qualite_p=row.get('qualite_p'),
            qualite_m=row.get('qualite_m'),
            transparence_score = row.get("transparence"),
            qualite_score=row.get("qualite")
        )
        session.add(quality_metrics)

    # Create the `ProcessType` instance
    process_type = ProcessType(
        emission_id=emission_data.emission_id,
        type_poste=row.get('type_poste'),
        nom_poste_francais=row.get('nom_poste_francais'),
        type_ligne=row.get('type_ligne'),
    )
    session.add(process_type)

def fill_models_from_dataframe(df: pd.DataFrame):
    """
    Group data by element_id, process it, and populate the database.
    """
    # Group by `element_id` to avoid creating duplicate `Element` entries
    grouped = df.groupby('identifiant_de_lelement')
    
    with SessionLocal() as session:
        for element_id, group in grouped:
            # Use the first row of each group for element-level data
            first_row = group.iloc[0]

            # Create or retrieve the `Element` instance
            element = Element(
                element_id=element_id,
                structure=first_row.get('structure'),
                statut_element=first_row.get('statut_element'),
                nom_base_francais=first_row.get('nom_base_francais'),
                code_categorie=first_row.get('code_categorie'),
                localisation=first_row.get('localisation_geographique'),
                sous_localisation=first_row.get("sous-localisation_geographique_français"),
            )
            session.merge(element)  # `merge` to avoid duplicates if `element_id` already exists should never be the case

            # Process each row within the group for `EmissionData` entries
            for _, row in group.iterrows():
                process_emission_row(row, element_id, session)

        # Commit all changes
        session.commit()
        print("All data has been successfully loaded into the database.")