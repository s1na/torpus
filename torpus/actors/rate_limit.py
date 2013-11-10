from pykka import ThreadingActor
from twython import TwythonRateLimitError


class RateLimitActor(ThreadingActor):

    def __init__(self, daemon_actor, twitter):
        ThreadingActor.__init__()
        self.daemon_actor = daemon_actor
        self.twitter = twitter

    def on_start(self):
        pass

    def on_receive(self, msg):
        resource_families = ','.join([resource.split('/')[0] for resource in msg])
        try:
            rate_limit = self.twitter.\
                    get_application_rate_limit_status(resources=resource_families)
        except TwythonRateLimitError as e:
            print e.msg
            self.daemon_actor.tell('stop')
        return rate_limit['resources']
