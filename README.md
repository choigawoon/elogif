# Elogif

Sort gif

# Setup

## Configuration

Modifiy settings.py or create environement variables.

| settings.py   | Environment Variable | default  | What for            |
| ------------- |:-------------:    |:-----:      |-----                |
| PORT          | ELOGIF_PORT       | 5555        |tornado listen port
| GIF_PATH      | ELOGIF_GIF_PATH   |   '{/path/to/script}/gif' | Gif files location|
| REDIS_HOST    | ELOGIF_REDIS_HOST |   'localhost' | Redis hostname         |
| REDIS_PORT    | ELOGIF_REDIS_PORT |   6379 | Redis port                    |
| REDIS_ZNAME   | ELOGIF_REDIS_ZNAME|   'elo-gif' | Hash id for score storage|


## Requierments
Elogif need a Redis database
`
pip install -r req.txt
`

## Launch

`
python server.py
`

# Docker usage

## Quick run

```
docker run --name elogif_redis -v /home/benco/elogif/data:/data -d redis redis-server --appendonly yes

docker run -p 55555:5555 --name elogif_backend --link elogif_redis:redis -e ELOGIF_REDIS_HOST=redis -v /home/benco/elogif/gif:/srv/gif -d totetmatt/elogif
```
## Build
`docker build -t <imagename> .`

# Usage
Select the gif you prefer by clicking on it or use the arrow on your keyboard (Left,Right to choose a winner, Up to declare a draw).
