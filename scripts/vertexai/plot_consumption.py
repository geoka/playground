import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Year'])

def plot_consumptions(df, entity):
    entity_data = df[df['Entity'] == entity]
    
    plt.figure(figsize=(10, 6))
    plt.plot(entity_data['Year'], entity_data['Wind consumption - TWh'], label='Wind Consumption')
    plt.plot(entity_data['Year'], entity_data['Solar consumption - TWh'], label='Solar Consumption')
    plt.plot(entity_data['Year'], entity_data['Hydro consumption - TWh'], label='Hydro Consumption')
    plt.plot(entity_data['Year'], entity_data['Oil consumption - TWh'], label='Oil Consumption')
    
    plt.title(f'Energy Consumption Over Time for {entity}')
    plt.xlabel('Year')
    plt.ylabel('Consumption (TWh)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def main():
    st.title('Energy Consumption Time Series')
    
    file_path = 'ETL-Renewable-Energy-Consumption/data/energy-consumption-by-source-and-country.csv'
    df = load_data(file_path)
    
    entities = df['Entity'].unique()
    selected_entity = st.selectbox('Select Entity', entities)
    
    plot_consumptions(df, selected_entity)

if __name__ == "__main__":
    main()
