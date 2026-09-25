PLANS = {"free": 0, "pro": 12, "team": 40}


def price(plan, seats=1):
    return PLANS[plan] * seats
