from bot.validators import validate_order_input

def build_order_payload(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None
):
    validate_order_input(order_type, price)

    payload = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"

    return payload
