import os

from src.data_processing.data_cleaning import clean_dataframe, load_data
from src.data_processing.upload_data import fill_models_from_dataframe
from src.database.db import Base, engine


def fill_database():
    Base.metadata.create_all(bind=engine)

    base_path_main = os.path.dirname(os.path.abspath(__file__))
    df = clean_dataframe(
        load_data(
            path=os.path.join(
                base_path_main, "..", "data", "donnees_candidats_dev_python.xlsx"
            )
        )
    )
    fill_models_from_dataframe(df)


if __name__ == "__main__":
    fill_database()
