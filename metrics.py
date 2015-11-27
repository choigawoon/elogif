import db
import datetime
class Stats:
    _GLOBAL_VOTE = "global_votes"
    _DAILY_VOTE  = "daily_votes"

    def __init__(self):
        self.db = db.get_connection()
    def inc_vote(self):
        print("lol")
        self.db.incr(self._GLOBAL_VOTE)
        self.db.incr(self._generate_daily_vote_id())
    def _generate_daily_vote_id(self):
        return "{}:{}".format(self._DAILY_VOTE,datetime.date.today().strftime("%Y-%m-%d"))
    def get_global_vote(self):
        return self.db.get(self._GLOBAL_VOTE)

stats = Stats()