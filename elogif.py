import os
import random
import uuid


import elo

import settings
import db
import metrics
class EloGif:
    def __init__(self):
        self.refresh_gifs()
        self.database = Database()
        self._valid_actions =['win','loose','draw']

    def refresh_gifs(self):
        self.list_gif = [ 
            {'full':os.path.join(settings.GIF_PATH,f),'name':f} for f in os.listdir(settings.GIF_PATH) if os.path.isfile(os.path.join(settings.GIF_PATH,f)) 
        ]

    def can_vote(self):
        return len(self.list_gif) >= 2

    def generate_vote(self):
        gif_left = random.choice(self.list_gif)
        gif_right = random.choice(self.list_gif)
        vote_id = uuid.uuid4().hex

        while gif_left['name'] == gif_right['name']:
            gif_right = random.choice(self.list_gif)

        vote_token = {"vote_id":vote_id, "gif_left":gif_left, "gif_right":gif_right}
        self.database.create_vote_token(**vote_token)
        return vote_token

    def vote(self,vote_id,gif_left,gif_right,action):
        if action not in self._valid_actions:
            return False

        if not self.database.check_vote(vote_id,gif_left,gif_right):
            return False

        if action == "win":
            self.database.fight(gif_left,gif_right)
        elif action == "loose":
            self.database.fight(gif_right,gif_left)
        else:
            self.database.draw(gif_left,gif_right)
        metrics.stats.inc_vote()
        return True

    def ranking(self,limit=50):
        return self.database.rank_list(limit)

    def random_pick(self,top_limit=-1):
        random_gif = random.choice(self.ranking(top_limit))

        return {
                "name":random_gif[0].decode('utf-8'),
                "score":random_gif[1]
               }

class Database:
    def __init__(self):
        self.r = db.get_connection()

    def rank_list(self,limit=50):
        if limit <=0:
            limit= 50
        return self.r.zrevrange(settings.REDIS_ZNAME,0,limit,withscores=True)
        
    def create_vote_token(self,vote_id,gif_left,gif_right):
        self.r.hset(vote_id,gif_left['name'],"unvoted")
        self.r.hset(vote_id,gif_right['name'],"unvoted")
        self.r.expire(vote_id,3600)

    def check_vote(self,vote_id,gif_left,gif_right):
        if self.r.hexists(vote_id,gif_left) and self.r.hexists(vote_id,gif_right):
            return True
        return False

    def set_score(self,gif_id,score):
        self.r.zadd(settings.REDIS_ZNAME,gif_id,score)

    def get_score(self,gif_id):
        score = self.r.zscore(settings.REDIS_ZNAME,gif_id)
        if score:
            return score
        return 1200

    def remove_gif_double(self,a,b):
        score_a = get_score(a)
        score_b = get_score(b)
        if score_a < score_b:
            self.delete(a)
        else:
            self.delete(b)

    def delete(self,gif_name):
        self.r.zrem(settings.REDIS_ZNAME,gif_name)

    def fight(self,win,loose):
        score_win = self.get_score(win)
        score_loose = self.get_score(loose)
        score_win_final, score_loose_final = elo.rate_1vs1(score_win,score_loose)
        self.set_score(win,float(score_win_final))
        self.set_score(loose,float(score_loose_final))

    def draw(self,a,b):
        score_a = self.get_score(a)
        score_b = self.get_score(b)
        final_score_a, final_score_b = elo.rate_1vs1(score_a,score_b,drawn=True)
        self.set_score(a,float(final_score_a))
        self.set_score(b,float(final_score_b))

app = EloGif()