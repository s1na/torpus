from collections import deque

from pykka import ThreadingActor
from twython import Twython

from torpus.config import *
from torpus.actors.rate_limit import RateLimitActor


class Daemon(ThreadingActor):

    def __init__(self):
        ThreadingActor.__init__()
        self.twitter = Twython(
            TWITTER_CONSUMER_KEY,
            access_token=TWITTER_ACCESS_TOKEN,
        )
        self.jobs = deque()
        self.used_apis = [
            'application/rate_limit_status',
        ]

    def on_start(self):
        rl_actor = RateLimitActor(self.actor_ref, self.twitter).start()
        self.rate_limits = rl_actor.ask(self.used_apis)

    def on_receive(self, msg):
        pass

    def on_stop(self):
        pass
