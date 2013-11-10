from pykka import ThreadingActor
from twython import TwythonError

from torpus.db import add_resource


class ResourceActor(ThreadingActor):

    def __init__(self, daemon_actor, twitter):
        ThreadingActor.__init__()
        self.daemon_actor = daemon_actor
        self.twitter = twitter

    def on_receive(self, msg):
        resource, args = msg.split(' ', 1)
        res = None

        try:
            if resource == 'users/show':
                res = self.twitter.show_user(*args)
            elif resource == 'users/lookup':
                res = self.twitter.lookup_user(*args)
        except TwythonError as e:
            print e.msg

        if res:
            ok = add_resource(res)
            if not ok:
                self.daemon_actor.tell('resource ' + msg)
        else:
            self.daemon_actor.tell('resource ' + msg)
