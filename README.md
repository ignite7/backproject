# Backproject 💎

This is an open source API project, the main idea is to bring together three services that nowadays people
consume every day as movies, series, games and music. For this was required to use external
databases which are [**_IMDb_**](https://imdb-api.com/api), [**_IGDB_**](https://api-docs.igdb.com/)
and [**_Spotify_**](https://developer.spotify.com/documentation/web-api/), you can see the
[**_docs_**](https://backproject.xyz/documentation/) if you want to know more, and the last but not
least I hope you like it as much as I did when I was writing the code!

## Setup 🧲

- If you want to try it on your own if easy to do it but is **important** you have to consider
the `.env` files of the project, inside each one I've commented the values you have to put in,
to run the project it takes two simple steps:

1. First step, make sure you have your own values.

```bash
1. backproject/.env
2. backproject/back/.env
3. backproject/api/services/.env
```

2. Second step, run the project with docker-compose.

```
cd backproject/
sudo docker-compose -f dev.yml up
```

## Tools used ⚙️

- Django REST framwork
- Docker
- Celery
- Flower
- Redis
- RabbitMQ
- Caddy
- MySQL
- AWS

## To do 🗝

- This project can be improved with more services taht people consume everyday, the good news is
we have the possibility to create a new world from our houses, so go ahead if you have an excelent
idea!

## Thanks 👏🏻

> **_Made By:_** [Sergio van Berkel Acosta](https://www.sergiovanberkel.com/)
