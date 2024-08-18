import pandas as pd
import numpy as np

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def preprocess_data(df):
    # Fill missing values (if any) with 0
    df.fillna(0, inplace=True)

     # Calculate percentage change in Coal consumption
    df['Coal consumption - % Change'] = df.groupby('Entity')['Coal consumption - TWh'].pct_change() * 100
    return df

def save_clean_data(df, output_filepath):
    df.to_csv(output_filepath, index=False)

if __name__ == "__main__":
    # Load the data
    filepath = 'ETL-Renewable-Energy-Consumption/data/energy-consumption-by-source-and-country.csv'
    df = load_data(filepath)

    # Preprocess the data
    df_clean = preprocess_data(df)

    # Save the cleaned data
    output_filepath = 'ETL-Renewable-Energy-Consumption/data/energy-consumption-by-source-and-country_clean.csv'
    save_clean_data(df_clean, output_filepath)
    print("Data preprocessing complete and saved to", output_filepath)
