from dataclasses import dataclass

@dataclass
class Event:
    def to_dict(self):
        return {"type": self.__class__.__name__, **self.__dict__}
    
    @staticmethod
    def from_dict(data):
        event_type = data.pop("type")
        if event_type == "OrderPlaced":
            return OrderPlaced(**data)
        elif event_type == "OrderCancelled":
            return OrderCancelled(**data)
        elif event_type == "TradeExecuted":
            return TradeExecuted(**data)
        elif event_type == "FundsDebited":
            return FundsDebited(**data)
        elif event_type == "FundsCredited":
            return FundsCredited(**data)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

@dataclass
class OrderPlaced(Event):
    order_id: int
    user_id: int
    buy_or_sell: str
    price: float
    quantity: int

@dataclass
class OrderCancelled(Event):
    order_id: int
    user_id: int

@dataclass
class TradeExecuted(Event):
    buy_order_id: int
    sell_order_id: int
    price: float
    quantity: int

@dataclass
class FundsDebited(Event):
    user_id: int
    amount: float
    message: str

@dataclass
class FundsCredited(Event):
    user_id: int
    amount: float
    message: str