from pykka import ThreadingActor


class RateLimitActor(ThreadingActor):

    def __init__(self, daemon_actor, twitter):
        ThreadingActor.__init__()
        self.daemon_actor = daemon_actor
        self.twitter = twitter

    def on_start(self):
        pass

    def on_receive(self, msg):
        resource_families = ','.join([resource.split('/')[0] for resource in msg])
        rate_limits = self.twitter.\
                get_application_rate_limit_status(resources=resource_families)
        return rate_limits['resources']
