import pandas as pd
import os
from sqlalchemy import create_engine


def excel_to_sqlite(excel_file, sqlite_file, table_name):
    # Read Excel file into a pandas DataFrame
    if excel_file.endswith('.csv'):
        df = pd.read_csv(excel_file)
    else:
        df = pd.read_excel(excel_file)

    # Create a SQLite engine
    engine = create_engine(f'sqlite:///{sqlite_file}')
    # Write DataFrame to SQLite database
    df.to_sql(table_name, engine, index=False, if_exists='replace')

    return df.columns.values, table_name, sqlite_file
