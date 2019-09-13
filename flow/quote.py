from logging import Logger
from flow import uuid4, random, datetime, json

from flow.user import User
from flow.transaction import Transaction

log = Logger("quote")


def _generate_fake_quote_data():
    rand_i, rand_j = random.random(), random.random()
    return {
        "type": "rent" if rand_i > 0.5 else "owner",
        "device": "web" if rand_j > 0.5 else "mobile"
    }

class Policy(object):
    def __init__(
        self,
        user_id,
        quote_id,
        policy_type,
        device,
        purchase_time,
    ):
        self.policy_id = str(uuid4())
        self.user_id = user_id
        self.quote_id = quote_id
        self.policy_type = policy_type
        self.policy_device = device
        self.purchase_time = purchase_time 

    def get(self):
        return self.__dict__


class Quote(object):
    """new quote initialized on the platform 
    if quotes are binded to user and paid it becomes a policy
    """
    def __init__(self,):
        """initializes a new unbounded quote with fake data

        """
        self.quote_id = str(uuid4())
        self.is_binded = False
        self.is_paid = True
        self.binding_date = None
        self.user_id = None
        self.creation_date = str(datetime.datetime.now())
        quote_data = _generate_fake_quote_data()
        self.quote_type = quote_data["type"]
        self.quote_device = quote_data["device"]
    
    
    def bind(self, user: User):
        if not self.is_binded:
            self.user_id = user.get_user_id()
            self.is_binded = True
            self.binding_date = str(datetime.datetime.now())
        else:
            log.warn("quote is alredy bounded, will not re-bind")
        

    def purchase(self, transaction: Transaction):
        if transaction.successful:
            self.is_paid = True


    def generate_policy(self,):
        return Policy(
            user_id=self.user_id,
            quote_id=self.quote_id,
            policy_type=self.quote_type,
            device=self.quote_device,
            purchase_time=str(datetime.datetime.now())
        )

    def get(self):
        return self.__dict__
