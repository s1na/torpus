from mongoengine import connect

from torpus.config import *
from torpus.daemon import Daemon

if __name__ == '__main__':
    connect('torpus')
    dmon = Daemon().start()
    dmon.ask('add_user %s' % SEED_USER)
