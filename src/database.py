import pandas as pd
from sqlalchemy import create_engine
from .config import CSV_FILE_PATH, DATABASE_FILE_PATH


def initialize_database():
    engine = create_engine(f"sqlite:///{DATABASE_FILE_PATH}")
    df = pd.read_csv(CSV_FILE_PATH).dropna(axis=1, how="all")
    df.to_sql("Person_Details", con=engine, if_exists="replace", index=False)
    return engine
