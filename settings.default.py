import os

PORT        = os.environ.get("ELOGIF_PORT",5555)

GIF_PATH    = os.environ.get("ELOGIF_GIF_PATH",os.path.join(os.getcwd(),'gif'))

REDIS_HOST  = os.environ.get("ELOGIF_REDIS_HOST","localhost")
REDIS_PORT  = os.environ.get("ELOGIF_REDIS_PORT","6379")
REDIS_ZNAME = os.environ.get("ELOGIF_REDIS_ZNAME","elo-gif")

DEBUG_MODE  = False