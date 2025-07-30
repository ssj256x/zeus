from pprint import pprint

from broker.fyers import FyersBroker

broker = FyersBroker()
pprint(broker.get_profile())