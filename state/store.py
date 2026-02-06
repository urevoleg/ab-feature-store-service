from abc import ABC, abstractmethod
from datetime import datetime


class StateStore(ABC):

    @abstractmethod
    def set_flag_once(self, user_id: str, name: str, ts: datetime):
        ...

    @abstractmethod
    def inc_metric(self, user_id: str, name: str, ts: datetime):
        ...
