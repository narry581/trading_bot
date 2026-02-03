def validate_order_input(order_type, price):
    if order_type == "LIMIT" and price is None:
        raise ValueError("Price is required for LIMIT orders")
