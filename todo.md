 - Experimental memo for db connection etc.
 - Tidy up code

 - Docker Compose
    - Dashboard
    - PostgreSQL database
        - Backup regularly
        - docker exec -t your-db-container pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
        - cat your_dump.sql | docker exec -i your-db-container psql -U postgres
    - Cron job scraping.

 - Extra:
    - Floorplans -> modelling
    - Extend rightmove-webscraper (add more images, let available date etc/). Need to understand XPaths.