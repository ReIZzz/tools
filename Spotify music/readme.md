Tool for collect yours music listened on Spotify with a renewable token setting & upload to database

- [`main`](https://github.com/ReIZzz/tools/blob/main/Spotify%20music/main.py) - module for load data & upload to DB
- [`refresh`](https://github.com/ReIZzz/tools/blob/main/Spotify%20music/refresh.py) – modul for receive new token

also you need module `secrets` with two string variables:

1. [**spotify_user_id**:**client_secrets**] encoding on _Base 64_
2. [refresh_token]
