import streamlit as st


from rightmove_scrape.get_from_db import get_property_data, get_search_urls
from rightmove_scrape.insert_to_db import insert_search, remove_duplicate_searches
from rightmove_scrape.scrape import main as scraping_main
from rightmove_scrape.schemas import get_db_session_maker
from create_db import main as create_db_main


st.title("Database explorer")

create_db_main()

data = get_property_data(get_db_session_maker())

searches = get_search_urls(get_db_session_maker())

with st.form("Re-do scrape"):
    submitted = st.form_submit_button("Scrape")
    if submitted:
        if len(searches):
            scraping_main()
            st.text("Scraping complete")
        else:
            st.text("No searches available. Add a search first.")

st.text("Insert search URL. This is begging for a SQL injection attack")
with st.form("New Search URL"):
    search_name = st.text_input("Search Name")
    search_url = st.text_input("Search URL")
    submitted = st.form_submit_button("Insert Search")
    if submitted:
        insert_search(get_db_session_maker(), search_name, search_url)
        st.text("Submitted :)")
        searches = get_search_urls(get_db_session_maker())
        remove_duplicate_searches(get_db_session_maker())


if len(searches):
    st.text("Current Searches")
    st.dataframe(searches)

if len(searches) and len(data):
    most_recent_date = data["search_date"].max()
    st.text(f"Most recent scrape: {most_recent_date}.")


else:
    st.write("No data in database or no searches available. Scrape first.")
