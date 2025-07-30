from .fyers import FyersBroker
from .base import AbstractBroker

BROKER_MAP = {
    "fyers": FyersBroker,
}

def get_broker(broker_name: str) -> AbstractBroker:
    if broker_name not in BROKER_MAP:
        raise ValueError(f"Broker '{broker_name}' not supported")
    return BROKER_MAP[broker_name]()