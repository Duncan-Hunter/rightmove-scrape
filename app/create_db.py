from rightmove_scrape.schemas import get_engine, metadata_obj

def main():
    metadata_obj.create_all(get_engine())

if __name__ == "__main__":
    main()