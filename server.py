import json
import os
import signal
import socket
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

import settings
import handlers
root = os.getcwd()

application = tornado.web.Application([
    (r"/",handlers.Home),
    (r"/rank",handlers.Rank),
    (r"/api/random", handlers.ApiRandom),
    (r"/api/random/(?P<top>\d+)", handlers.ApiTop),
    (r"/api/refresh", handlers.ApiRefresh),
    (r"/gif/(.*)", tornado.web.StaticFileHandler, {"path": settings.GIF_PATH}),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": '{}/static'.format(root), "default_filename": "index.html"})
],debug=True,template_path="{}/templates/".format(root))
application.clients = []

def sig_handler(sig, frame):

    tornado.ioloop.IOLoop.instance().stop()
    stream.disconnect()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(settings.PORT)
    
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    myIP = socket.gethostbyname(socket.gethostname())
    myIP = "localhost"
    logging.info('*** Websocket Server Started at %s***' % myIP )
    tornado.ioloop.IOLoop.instance().start()