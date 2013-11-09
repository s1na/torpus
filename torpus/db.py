from mongoengine import Document, StringField, ListField

class DaemonModel(Document):
    jobs = ListField(StringField())

    def append_job(self, job):
        self.jobs.append(job)

    def pop_job(self, job):
        return self.jobs.pop(0)

#class User(Document):
#    screen_name = StringField(required=True)
