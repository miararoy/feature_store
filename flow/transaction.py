from flow import random, Factory, uuid4, json, datetime
from flow.user import User

fake = Factory.create()


class PaymentMethod(object):
    def __init__(self):
        self.card_number = fake.credit_card_number()
        self.card_expiration_date = fake.credit_card_expire()
        self.card_type = "debit" if random.random() > 0.8 else "credit"

    def process_random_payment(self):
        if random.random() > 0.2:
            return True
        else:
            return False        


class Transaction(object):
    def __init__(
        self,
        user: User,
        payment_method: PaymentMethod,
        ref_id: str = None,
        ref_type: str = None
    ):
        self.transaction_id = str(uuid4())
        self.user_id = user.get_user_id()
        self.successful = payment_method.process_random_payment()
        self.transaction_time = str(datetime.datetime.now())
        self.card_number = payment_method.card_number[:4] + "********" + payment_method.card_number[-4:]
        self.card_expiration_date = payment_method.card_expiration_date
        self.card_type = payment_method.card_type
        self.ref_id = ref_id
        self.ref_type = ref_type
    
    def get_transaction_id(self):
        return self.transaction_id

    def get(self):
        return self.__dict__