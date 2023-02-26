from rightmove_scrape.schemas import SEARCH, PROPERTY, get_engine
from uuid import uuid4
from sqlalchemy import func


# Insert row into search postgres table
def insert_search(_session_maker, search_name, search_url):
    with _session_maker.begin() as session:
        # session.add(SEARCH(search_name=search_name, search_url=search_url))
        insert_statement = SEARCH.insert().values(id=str(uuid4()),
                                                  name=search_name,
                                                  search_url=search_url)
        session.execute(insert_statement)
        session.commit()
        return


# Insert dataframe into property postgres table
def insert_properties(df):
    engine = get_engine()
    df.to_sql(PROPERTY.name, engine, if_exists="append", index=False)
    return


# remove extra duplicate rows from Property table in Postgres
def remove_duplicates(_session_maker):
    with _session_maker.begin() as session:
        session.execute(f"""
        DELETE FROM {PROPERTY.name} a USING (
            SELECT MIN(ctid) as ctid, rightmove_id, search_date
        FROM {PROPERTY.name} 
        GROUP BY rightmove_id, search_date HAVING COUNT(*) > 1
        ) b
        WHERE a.rightmove_id = b.rightmove_id 
        AND a.search_date = b.search_date
        AND a.ctid <> b.ctid;
        """)
        session.commit()


def remove_duplicate_searches(_session_maker):
    with _session_maker.begin() as session:
        session.execute(f"""
        DELETE FROM {SEARCH.name} a USING (
            SELECT MIN(ctid) as ctid, name, search_url
        FROM {SEARCH.name} 
        GROUP BY name, search_url HAVING COUNT(*) > 1
        ) b
        WHERE a.name = b.name 
        AND a.search_url = b.search_url
        AND a.ctid <> b.ctid;
        """)
        session.commit()
