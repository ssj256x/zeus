from broker.base import AbstractBroker
from broker.factory import get_broker


def on_connect():
    print(f'Connected!')


def on_message(msg):
    print(f'Tick : {msg}')


def on_close(msg):
    print(f'Close : {msg}')


def on_error(msg):
    print(f'Error: {msg}')


broker: AbstractBroker = get_broker('fyers')
symbols = ['NSE:NIFTY50-INDEX']
broker.stream_ticker(
    symbols,
    write_to_file=False,
    on_connect=on_connect,
    on_message=on_message,
    on_close=on_close,
    on_error=on_error,
)
