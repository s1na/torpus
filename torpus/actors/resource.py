from pykka import ThreadingActor


class ResourceActor(ThreadingActor):

    def __init__(self, daemon_actor, twitter):
        ThreadingActor.__init__()
        self.daemon_actor = daemon_actor
        self.twitter = twitter

    def on_receive(self, msg):
        resource, args = msg.split(' ', 1)
        res = None

        if resource == 'users/show':
            res = self.twitter.show_user(*args)
        elif resource == 'users/lookup':
            res = self.twitter.lookup_user(*args)

        # If good res, add to db.
