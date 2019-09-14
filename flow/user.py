from flow import random, Factory, uuid4, datetime, json, time

fake = Factory.create()

class User(object):
    def __init__(self,):
        self.user_id = str(uuid4())
        self.creation_date = time()
        self.name = fake.name()
        self.address = fake.address().replace('\n', ' ')

    def get_user_id(self):
        return self.user_id
    
    def get(self):
        return self.__dict__
        