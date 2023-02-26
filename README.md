# Rightmove webscraping and dashboard

A side project to track property prices and some other stats, using the `rightmove-webscraper` library.

Uses Streamlit and Postgres with docker compose.

It's designed to be set up on a raspberry pi, with a micro sd card for data storage and an internet connection. If you have a linux server it's probably fairly simple to set up on that, might even be easy on AWS but I haven't tested it.

A word of warning, it's not allowed to use that library, so *don't*.

## Set up
This is designed to use docker compose. I'll add a link to how to install that later.

## Build scrape app image
In the future I could push this to some public repository, but really I won't because of the way searches are inserted into the database.

```
$sudo docker build -t scrape_app .
```

## Set up environment variables
```
$cp env .env
```
Change the variables in the new `.env` file to what you want. Some understanding of what they mean is helpful, I can add documentation later.
`POSTGRES_VOLUME` is where the postgres database data will be persisted locally.

## Run docker compose
This sets up a local postgres database and runs the streamlit app. This uses the environment variables as above.

```
$sudo docker compose up
```

Then go to `http://0.0.0.0:8501` to see the dashboard. This might need some extra steps for connecting to it from a computer other than the host.
