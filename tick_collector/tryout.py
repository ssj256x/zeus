from pprint import pprint

from broker.base import AbstractBroker
from broker.factory import get_broker

broker: AbstractBroker = get_broker('fyers')
pprint(broker.get_profile())
