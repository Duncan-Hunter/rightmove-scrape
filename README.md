# Rightmove webscraping and dashboard

A side project to track property prices and some other stats, using the `rightmove-webscraper` library.

A word of warning, it's not allowed to use that library, so *don't*.

## Set up
I'll be adding docker containers.

### poetry
cd to the cloned directory and run

`poetry install`

### postgres db

`cp env .env`

Fill in the fields.

You can run

`poetry run python create_db.py`

It might not work yet. It should use the details in `.env`. I really recommend this for home use only and localhosting.

### Streamlit

`poetry run streamlit run app/main_page.py`
