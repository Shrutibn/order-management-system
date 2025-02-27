# function to create order_id
def get_order_id(row_id, prefix='ORD'):
    order_id = prefix + str(hex(row_id + 1000000))[3:]
    return order_id