from rightmove_webscraper import RightmoveData
from time import sleep
from datetime import datetime
import pandas as pd
import unicodedata
import uuid

from rightmove_scrape.get_from_db import get_search_urls
from rightmove_scrape.schemas import get_db_session_maker
from rightmove_scrape.insert_to_db import remove_duplicates, insert_properties


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")


def process_df(scraped):
    scraped["rightmove_id"] = scraped["url"].str.split("/").apply(lambda x: x[-2]).str.strip('#')
    scraped["number_bedrooms"] = scraped["number_bedrooms"].fillna(-1).astype(int)
    scraped["type"] = scraped["type"].apply(remove_control_characters)
    scraped["address"] = scraped["address"].apply(remove_control_characters)
    scraped = scraped.drop(columns=["full_postcode"])
    scraped = scraped.drop_duplicates(subset=["rightmove_id", "search_id"])
    current_time = datetime.now().strftime("%H:%M:%S")
    scraped["search_time"] = current_time
    scraped["id"] = scraped.apply(lambda _: uuid.uuid4(), axis=1)
    return scraped
    

def main():
    searches = get_search_urls(get_db_session_maker())
    print(searches)
    dfs = []
    for search_id, row in searches.iterrows():
        rm = RightmoveData(row.search_url)
        df = rm.get_results
        df["search_id"] = search_id
        print(row.name, " Number of properties: ", len(df))
        dfs.append(df)
        sleep(5)

    scraped = pd.concat(dfs, axis=0)
    
    results = process_df(scraped)
    results.to_csv("recent_scrape.csv", index=False)
    insert_properties(results)
    remove_duplicates(get_db_session_maker())


if __name__ == "__main__":
    main()
