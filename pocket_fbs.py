# pocket_fbs.py
from utils.session import validate_session
from trade.order import place_order

print(">> Connected to Pocket Option")

if validate_session():
    print(">> Session validated. Executing trade...")
    place_order()  # default: EURUSD_otc, $5, call, demo
else:
    print(">> Session invalid or expired. Terminating bot.")

print(">> Disconnected from Pocket Option")
