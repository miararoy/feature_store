from flow import time, random
from flow.quote import Quote
from flow.user import User
from flow.transaction import Transaction, PaymentMethod

class EmptyAttr():
    def get(self):
        return None

def get_single_flow():
    quote = Quote()
    user = EmptyAttr()
    trans = EmptyAttr()
    policy = EmptyAttr()
    if random.random() > 0.2:
        user = User()
        quote.bind(user)

        if random.random() > 0.2:
            payment_method = PaymentMethod()
            trans = Transaction(user, payment_method)
            quote.purchase(trans)
            policy = quote.generate_policy()

    return quote.get(), user.get(), trans.get(), policy.get()
    