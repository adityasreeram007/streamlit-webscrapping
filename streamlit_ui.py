import streamlit as st
import pandas as pd
import sqlite3
from db_actions import load_data , get_first_n_rows


def main():
    get_first_n_rows()
    st.title('Bus Routes')

    df = load_data()
    df['price'] = df['price'].apply(lambda x: float(x.split(' ')[-1]))
    # Filter options
    df['star_rating'] = df['star_rating'].astype(float)
    unique_bustypes = df['bustype'].unique()
    selected_bustype = st.sidebar.multiselect('Bus Type', unique_bustypes, unique_bustypes)

    unique_routes = df['route_name'].unique()
    selected_route = st.sidebar.multiselect('Route', unique_routes, unique_routes)

    min_price, max_price = st.sidebar.slider('Price Range', float(df['price'].min()), float(df['price'].max()), (float(df['price'].min()), float(df['price'].max())))

    min_rating, max_rating = st.sidebar.slider('Star Rating', float(df['star_rating'].min()), float(df['star_rating'].max()), (float(df['star_rating'].min()), float(df['star_rating'].max())))

    # Filter dataframe
    df = df[(df['bustype'].isin(selected_bustype)) & 
            (df['route_name'].isin(selected_route)) & 
            (df['price'].between(min_price, max_price)) & 
            (df['star_rating'].between(min_rating, max_rating))]

    # Display dataframe
    # Display dataframe
    st.table(df)

if __name__ == "__main__":
    main()