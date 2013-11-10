#from mongoengine import Document, StringField, ListField
from neo2py import neo4j

from torpus.config import NEO4J_CONFIG


db = neo4j.GraphDatabaseService(NEO4J_CONFIG)

def add_resource(data):
    pass


#class DaemonModel(Document):
    #jobs = ListField(StringField())

    #def append_job(self, job):
        #self.jobs.append(job)

    #def pop_job(self, job):
        #return self.jobs.pop(0)

#class UserModel(Document):
    #name = StringField()
    #created_at = DateTimeField()
    #location = StringField()
    #id_str = StringField(required=True)
    #favourites_count = IntField()
    #url = StringField()
    #utc_offset = IntField()
    #listed_count = IntField()
    #lang = StringField()
    #followers_count = IntField()
    #protected = BooleanField(default=False)
    #verified = BooleanField()
    #time_zone = StringField()
    #description = StringField()
    #statuses_count = IntField()
    #friends_count = IntField()
    #screen_name = StringField(required=True)

    #@classmethod
    #def add_if_not_exists(cls, user_data):
        #if not cls.objects(id_str == user_data['id_str']):
            #user = cls(id_str=user_data['id_str'], screen_name=user_data['screen_name'])
            #attrs = inspect.getmembers(cls, lambda member:not(inspect.isroutine(member)))
            #attrs = [a[0] for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]
            #for attr in attrs:
                #setattr(user, attr, user_data[attr])
            #user.save()
#        return True
