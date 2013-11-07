from time import sleep

from pykka import ThreadingActor


class TimerActor(ThreadingActor):

    def __init__(self, daemon_actor, repeat=False):
        ThreadingActor.__init__()
        self.daemon_actor = daemon_actor
        self.repeat = repeat

    def on_receive(self, msg):
        sleep(msg)
        daemon_actor.tell(
            'timer%s' % (' repeat' if self.repeat else '')
        )


