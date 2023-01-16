from rightmove_scrape.schemas import get_engine, metadata_obj

if __name__ == "__main__":
    metadata_obj.create_all(get_engine())