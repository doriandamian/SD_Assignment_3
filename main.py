from events import *
from event_store import EventStore
from managers import OrderManager, AccountManager
from command_handlers import *

store = EventStore()
events = store.get_all_events()

order_manager = OrderManager()
account_manger = AccountManager()

order_manager.load_from_events(events)
account_manger.load_from_events(events)

store.append(FundsCredited(user_id="user1", amount=1000, message="Initial Funds"))

account_manger.load_from_events(store.get_all_events())

buy_id = place_order(store, account_manger, "user1", "buy", price=20, quantity=10)

events = store.get_all_events()
order_book = OrderManager() 
account_mgr = AccountManager()
order_book.load_from_events(events)
account_mgr.load_from_events(events)

print("Buy Orders:", order_book.buy_orders)
print("Sell Orders:", order_book.sell_orders)
print("Balances:", account_mgr.balances)