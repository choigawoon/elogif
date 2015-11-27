import json
import logging

import tornado.web

import elogif
import metrics
class Home(tornado.web.RequestHandler):
    def get(self):
        vote_id  = self.get_argument('key', None)
        if vote_id:
                gif_left = self.get_argument('gif_left', None)
                gif_right= self.get_argument('gif_right', None)
                action   = self.get_argument('action', None)
                elogif.app.vote(vote_id,gif_left,gif_right,action)
        if elogif.app.can_vote():
            vote = elogif.app.generate_vote()
            self.render('index.html',**vote)
        else:
            self.render('empty.html',info="No enough image")

class Rank(tornado.web.RequestHandler):
    def get(self):
            rank = elogif.app.ranking()
            nb_votes = metrics.stats.get_global_vote()
            self.render('rank.html',rank=rank,nb_votes=nb_votes)

class ApiRandom(tornado.web.RequestHandler):
    def get(self):
            rank = elogif.app.random_pick()
            rank["path"]="http://{hostname}/gif/{name}".format(hostname=self.request.host,name=rank['name'])
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(rank))

class ApiTop(tornado.web.RequestHandler):
    def get(self,top=10):
            rank = elogif.app.random_pick(top_limit=int(top))
            rank["path"]="http://{hostname}/gif/{name}".format(hostname=self.request.host,name=rank['name'])
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(rank))

class ApiRefresh(tornado.web.RequestHandler):
    def get(self):
            elogif.app.refresh_gifs()
            self.set_status(204)