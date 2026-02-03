import argparse
import logging
import os

from bot.client import BinanceFuturesClient
from bot.orders import build_order_payload
from bot.logging_config import setup_logging

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True, help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float, help="Required for LIMIT orders")

    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("Set BINANCE_API_KEY and BINANCE_API_SECRET env vars")

    client = BinanceFuturesClient(api_key, api_secret)

    try:
        order_payload = build_order_payload(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print("\nOrder Request:")
        for k, v in order_payload.items():
            print(f"  {k}: {v}")

        response = client.place_order(**order_payload)

        print("\nOrder Response:")
        print(f"  orderId: {response.get('orderId')}")
        print(f"  status: {response.get('status')}")
        print(f"  executedQty: {response.get('executedQty')}")
        print(f"  avgPrice: {response.get('avgPrice', 'N/A')}")

        print("\n✅ Order placed successfully")

    except Exception as e:
        logger.exception("Order failed")
        print(f"\n❌ Order failed: {e}")

if __name__ == "__main__":
    main()
