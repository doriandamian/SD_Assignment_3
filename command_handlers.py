import uuid
from events import *
from event_store import EventStore
from managers import AccountManager

def place_order(event_store: EventStore, account_manager: AccountManager, user_id: str, side: str, price: float, quantity: int):
    order_id = str(uuid.uuid4())
    cost = price * quantity

    if side == "buy" and account_manager.balances.get(user_id, 0) < cost:
        raise ValueError("Not enough funds")
    if side == "buy":
        event_store.append(FundsDebited(user_id, cost, f"Buy order {order_id}"))

    event_store.append(OrderPlaced(order_id, user_id, side, price, quantity))
    return order_id

def cancel_order(event_store: EventStore, order_id: str, user_id: str):
    event_store.append(OrderCancelled(order_id, user_id))

def execute_trade(event_store: EventStore, buy_order: OrderPlaced, sell_order: OrderPlaced):
    quantity = sell_order.quantity
    price = sell_order.price
    cost = quantity * price

    event_store.append(TradeExecuted(buy_order, sell_order, price, quantity))
    event_store.append(FundsCredited(sell_order.user_id, cost, f"Sell order {sell_order}"))