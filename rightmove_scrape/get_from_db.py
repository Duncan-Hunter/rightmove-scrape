from psycopg2 import connect
import pandas as pd
from decouple import config
from rightmove_scrape.schemas import SEARCH, PROPERTY, get_db_session_maker
import streamlit as st


# Get the search urls from Postgres, cache them, and return them as a dataframe
@st.experimental_memo
def get_search_urls(_session_maker=None):
    with _session_maker.begin() as session:
        searches = session.query(SEARCH).all()
        searches = pd.DataFrame(searches)
        if len(searches):
            searches.set_index("id", inplace=True, drop=True)
            return searches
        return pd.DataFrame()


# Get property data from Postgres, cache it, and return it as a dataframe
@st.experimental_memo
def get_property_data(_session_maker=None):
    with _session_maker.begin() as session:
        property_data = session.query(PROPERTY).all()
        property_data = pd.DataFrame(property_data)
        return property_data


if __name__== "__main__":
    PASSWORD = config("DBPASSWORD")
    get_search_urls(get_db_session_maker())
