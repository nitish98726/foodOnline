from datetime import datetime


def generate_order_number(pk):
    now = datetime.now()
    current_date = (now.strftime(r"%Y%m%d%H%M%S"))
    order_number = current_date + str(pk)
    return order_number