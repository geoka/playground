import sqlite3
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool,SingletonThreadPool



def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

def create_db_file():
    # File paths (adjust to your file location)
    csv_file_path = './data/energy-consumption-by-source-and-country_clean.csv'  # Replace with your CSV file path
    db_file_path = 'data/energy_data.db'  # Replace with your desired SQLite database file name

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Define the table schema
    table_name = 'energy_consumption'
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            Entity TEXT,
            Code TEXT,
            Year INTEGER,
            Other_renewables_TWh REAL,
            Biofuels_consumption_TWh REAL,
            Solar_consumption_TWh REAL,
            Wind_consumption_TWh REAL,
            Hydro_consumption_TWh REAL,
            Nuclear_consumption_TWh REAL,
            Gas_consumption_TWh REAL,
            Coal_consumption_TWh REAL,
            Oil_consumption_TWh REAL,
            Coal_consumption_percent_change REAL
        )
    ''')

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Rename columns to match the SQL schema (replace spaces and special characters)
    df.columns = [
        'Entity', 'Code', 'Year', 
        'Other_renewables_TWh', 
        'Biofuels_consumption_TWh', 
        'Solar_consumption_TWh', 
        'Wind_consumption_TWh', 
        'Hydro_consumption_TWh', 
        'Nuclear_consumption_TWh', 
        'Gas_consumption_TWh', 
        'Coal_consumption_TWh', 
        'Oil_consumption_TWh', 
        'Coal_consumption_percent_change'
    ]

    # Insert the DataFrame into the SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()

    print(f"Data loaded successfully into {db_file_path}")

def get_engine_for_energy_data():
    """
    Creates an SQLAlchemy engine.

    :param db_path: The database connection string.
                    Default is for a SQLite database named 'energy.db'.
                    For in-memory database use 'sqlite:///:memory:'.
    :return: SQLAlchemy engine object.
    """

    db_file = 'data/energy_data.db'
    # Connect to the disk-based database
    disk_conn = sqlite3.connect(db_file) # works OK
    # cursor = disk_conn.cursor()
    # print("Database created and Successfully Connected to SQLite")

    # Create an in-memory database
    # memory_conn = sqlite3.connect(':memory:')
  
    # Attach the disk-based database to the in-memory database
    # disk_conn.backup(memory_conn)

    # Close the connection to the disk-based database
    # disk_conn.close()

    print("Loaded energy.db into memory.")

    engine = create_engine(
        "sqlite://",
        creator=lambda: disk_conn,
        poolclass=SingletonThreadPool,
        connect_args={"check_same_thread": False},
    )


    # Get a list of all tables in the database
    # inspector = inspect(engine)

    # tables = inspector.get_table_names()
    # print(tables)

    return engine



if __name__ == "__main__":
    # Load data for first time
    # create_db_file()
    get_engine_for_energy_data()