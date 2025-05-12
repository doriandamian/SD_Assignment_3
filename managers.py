from typing import List
from events import *

class OrderManager:
    def __init__(self):
        self.buy_orders = {}
        self.sell_orders = {}

    def apply(self, event: Event):
        if isinstance(event, OrderPlaced):
            if event.buy_or_sell == "buy":
                self.buy_orders[event.order_id] = event
            else:
                self.sell_orders[event.order_id] = event
        elif isinstance(event, OrderCancelled):
            self.buy_orders.pop(event.order_id, None)
            self.sell_orders.pop(event.order_id, None)
        elif isinstance(event, TradeExecuted):
            self.buy_orders.pop(event.buy_order_id, None)
            self.sell_orders.pop(event.sell_order_id, None)

    def load_from_events(self, events: List[Event]):
        for event in events:
            self.apply(event)

class AccountManager:
    def __init__(self):
        self.balances = {}

    def apply(self, event: Event):
        if isinstance(event, FundsDebited):
            self.balances[event.user_id] = self.balances.get(event.user_id, 0) - event.amount
        elif isinstance(event, FundsCredited):
            self.balances[event.user_id] = self.balances.get(event.user_id, 0) + event.amount

    def load_from_events(self, events: List[Event]):
        for event in events:
            self.apply(event)