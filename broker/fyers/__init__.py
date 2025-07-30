from broker.base import AbstractBroker
from .config import get_fyers_data_socket, init_broker, get_fyers_model


class FyersBroker(AbstractBroker):
    def __init__(self):
        init_broker()

    def stream_ticker(self, symbol, **kwargs):
        ws = get_fyers_data_socket(**kwargs)
        ws.connect()
        ws.subscribe(symbols=[symbol], data_type='SymbolUpdate')
        ws.keep_running()

    def place_trade(self, trade):
        pass

    def exit_trade(self, trade):
        pass

    def get_all_trades(self):
        pass

    def get_all_open_trades(self):
        pass

    def get_profile(self) -> dict:
        fyers = get_fyers_model()
        return fyers.get_profile()
