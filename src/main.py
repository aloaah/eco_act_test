from dotenv import load_dotenv
load_dotenv(override=True)

import os

from src.data_processing.data_cleaning import clean_dataframe, load_data
from src.data_processing.upload_data import fill_models_from_dataframe
from src.database.db import Base, engine
Base.metadata.create_all(bind=engine)

def main_entrypoint():
    base_path_main = os.path.dirname(os.path.abspath(__file__))
    df = clean_dataframe(load_data(path=os.path.join(base_path_main, "..", "data", "donnees_candidats_dev_python.xlsx")))
    df.to_csv(os.path.join(base_path_main, "..", "data", "cleaned_data_dev_python.csv",), index=False)
    fill_models_from_dataframe(df)


if __name__ == "__main__":
    main_entrypoint()