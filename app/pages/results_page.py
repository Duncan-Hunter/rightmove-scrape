import sys
sys.path.insert(0, "..")

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from rightmove_scrape.get_from_db import get_search_urls, get_property_data, get_db_session_maker

sns.set_style("darkgrid")

st.title("Results")

data = get_property_data(get_db_session_maker())
searches = get_search_urls(get_db_session_maker())

if len(data):

    dataset = pd.merge(data, searches, how="left", left_on="search_id", right_on="id").sort_values(by=["rightmove_id", "search_date"], ascending=False)

    buy_or_rent = st.radio("Buy or Rent", options=["Buy", "Rent"])

    if buy_or_rent == "Buy":
        dataset = dataset[dataset["price"] > 3000]
    else:
        dataset = dataset[dataset["price"] < 3000]

    fig, axs = plt.subplots(1, 1, figsize=(10, 7.5))
    sns.stripplot(data=dataset, x="price", y="name", hue="number_bedrooms", ax=axs, palette="bright")

    st.pyplot(fig)

    fig, axs = plt.subplots(1, 1, figsize=(10, 7.5))
    sns.violinplot(data=dataset, x="price", y="name", hue="number_bedrooms", ax=axs, palette="bright")

    st.pyplot(fig)


    search_options = list(dataset["name"].unique())
    search_choice = st.selectbox("Search filter", options=search_options)

    filtered_dataset = dataset[dataset["name"] == search_choice]

    st.dataframe(filtered_dataset)

    fig, axs = plt.subplots(1, 1, figsize=(10, 7.5))
    sns.lineplot(data=filtered_dataset, x="search_date", y="price", hue="name", style="number_bedrooms", ax=axs, sort=True)

    st.pyplot(fig)

    fig, axs = plt.subplots(1, 1, figsize=(10, 7.5))
    sns.lineplot(data=filtered_dataset, x="search_date", y="price", hue=filtered_dataset["rightmove_id"].astype(str), style=filtered_dataset["rightmove_id"].astype(str), markers=True, ax=axs, legend=False)

    st.pyplot(fig)

    # dataset["rank"] = dataset.groupby("rightmove_id", sort=False)["search_date"].rank(method="first")
    # dataset = dataset[dataset["rank"] == 1]


    counts = dataset.groupby(['name', 'number_bedrooms', 'search_date']).count().sort_values(by=["name", "search_date"], ascending=True)
    counts["Number of properties"] = counts["price"]

    fig, axs = plt.subplots(1, 1, figsize=(10, 7.5))
    sns.lineplot(data=counts, x="search_date", y="Number of properties", hue="number_bedrooms", style="name", markers=True, ax=axs, sort=True, palette="bright")

    st.pyplot(fig)

else:
    st.text("No data to display, Scrape first.")