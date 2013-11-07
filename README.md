torpus
======

Torpus gives you the ability to gather tweets, we use it for data science purposes.

Usage
-----

After cloning the repository, install the requirements. Also I recommend using
virtualenv.

```
git clone git@github.com:s1na/torpus.git
cd torpus

sudo pip install -r requirements.pip
```

Then you need to get your access token, open a python shell:

```
from twython import Twython

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
```

write the ACCESS_TOKEN to the config file.

