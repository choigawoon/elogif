# Elogif

Sort gif

# Setup

## Configuration

Modifiy settings.py or create environement variables

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

With default settings.

`
docker run -d -p --name elogif_redis redis 
docker run -d -p 80:5555 --link elogif_redis:redis elogif/backend 
`

# Usage
Select the gif you prefer by clicking on it or use the arrow on your keyboard (Left,Right to choose a winner, Up to declare a draw).
