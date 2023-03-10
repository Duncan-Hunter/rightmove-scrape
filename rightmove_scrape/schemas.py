from sqlalchemy import Table, Column

from sqlalchemy import String, Date, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st

from rightmove_scrape.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_HOST, POSTGRES_DB


ENGINE_STR = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


@st.experimental_singleton
def get_db_session_maker():
    engine = create_engine(ENGINE_STR)
    return sessionmaker(engine)


@st.experimental_singleton
def get_engine():
    engine = create_engine(ENGINE_STR)
    return engine


metadata_obj = MetaData()


PROPERTY = Table(
    "property",
    metadata_obj,
    Column("price", Integer) ,
    Column("type", String(250)),
    Column("address", String(250)),
    Column("url", String(500)),
    Column("agent_url", String(250)),
    Column("postcode", String(10)),
    Column("number_bedrooms", Integer),
    Column("search_date", Date),
    Column("rightmove_id", Integer),
    Column("search_id", UUID),
    Column("search_time", Time),
    Column("id", UUID, primary_key=True)
)

SEARCH = Table(
    "search",
    metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("name", String(250)),
    Column("search_url", String(500))
)
