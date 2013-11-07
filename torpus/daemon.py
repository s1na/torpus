from collections import deque
import datetime

from pykka import ThreadingActor
from pykka import ActorRegistery
from twython import Twython

from torpus.config import *
from torpus.actors.rate_limit import RateLimitActor
from torpus.actors.timer import TimerActor
from torpus.actors.resource import ResourceActor


class Daemon(ThreadingActor):

    def __init__(self):
        ThreadingActor.__init__()
        self.twitter = Twython(
            TWITTER_CONSUMER_KEY,
            access_token=TWITTER_ACCESS_TOKEN,
        )
        self.jobs = deque()
        self.used_resources = [
            'application/rate_limit_status',
        ]
        self.rate_limit = {}
        self.local_remainings = {}
        self.reset_timers = {}

    def _active_actors(self, cls=None):
        if not cls:
            return ActorRegistery.get_all()
        else:
            return ActorRegistery.get_by_class(cls)

    def _update_rate_limit(self):
        rl_actor = RateLimitActor(self.actor_ref, self.twitter).start()
        rate_limit = rl_actor.ask(self.used_resources)

        for resource_family in rate_limit:
            for resource in resource_family:
                local_count = self.local_remainings.get(resource, None)
                remote_count = int(
                    rate_limit[resource_family][resource]['remaining']
                )
                if not local_count:
                    self.local_remainings[resource] = remote_count
                else:
                    if local_count != remote_count and local_count > remote_count:
                        print '[Daemon] Local count %d is more than\
                                remote on %d.' % (local_count, remote_count)
                        self.local_remainings[resource] = remote_count
                if self.reset_timers.get(resource, None):
                    self.reset_timers[resource].stop()
                timer_actor = TimerActor(self.actor_ref).start()
                timer_actor.tell(int(
                    rate_limit[resource_family][resource]['reset']
                ))
                self.reset_timers[resource] = timer_actor

    def on_start(self):
        self._update_rate_limit()

        rl_timer = TimerActor(self.actor_ref, repeat=True).start()
        rl_timer.tell(30)

    def on_receive(self, msg):
        actor = msg.split(' ', 1)[0]
        msg = msg.split(' ', 1)[1:]
        if actor == 'resource':
            if not len(msg):
                print '[Daemon] msg from resource is empty.'
                return False
            self.jobs.append(msg)
            if len(self._active_actors(ResourceActor)) <= ACTIVE_ACTOR_LIMIT:
                resource = msg.split(' ', 1)[0]
                resource_family = resource.split('/')[0]
                if int(self.local_remainings[resource]) >= 5:
                    resource_actor = ResourceActor(
                        self.actor_ref, self.twitter
                    ).start()
                    resource_actor.tell(self.jobs.pop())
                else:
                    self._update_rate_limit()
        if actor == 'timer':
            if msg == 'repeat':
                if len(self.jobs) > 0:
                    if len(self._active_actors(ResourceActor)) <\
                       ACTIVE_ACTOR_LIMIT:
                        self._do_job()
                else:
                    if len(self._active_actors(ResourceActor)) == 0:
                        print '[Daemon] Nothing to do, exiting.'
                        self.stop()
                        return False
            else:
                self._update_rate_limit()

    def on_stop(self):
        pass
