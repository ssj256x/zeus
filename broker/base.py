from abc import ABC, abstractmethod


class AbstractBroker(ABC):
    @abstractmethod
    def stream_ticker(self, symbol: str, **kwargs):
        pass

    @abstractmethod
    def place_trade(self, trade):
        pass

    @abstractmethod
    def exit_trade(self, trade):
        pass

    @abstractmethod
    def get_all_trades(self):
        pass

    @abstractmethod
    def get_all_open_trades(self):
        pass

    @abstractmethod
    def get_profile(self):
        pass