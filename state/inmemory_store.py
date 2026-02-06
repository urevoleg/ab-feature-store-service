from collections import defaultdict
from datetime import datetime

from pprint import pprint

from state.store import StateStore


class InMemoryStateStore(StateStore):
    def __init__(self):
        # date -> user_id -> data
        self.state = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "flags": set(),
                    "metrics": defaultdict(int),
                }
            )
        )

    def _date(self, ts: datetime) -> str:
        return ts.strftime("%Y-%m-%d")

    def set_flag_once(self, user_id: str, name: str, ts: datetime):
        date = self._date(ts)
        print(f'FLAG: -> {name}')
        self.state[date][user_id]["flags"].add(name)

    def inc_metric(self, user_id: str, name: str, ts: datetime):
        date = self._date(ts)
        self.state[date][user_id]["metrics"][name] += 1

    # удобный хелпер для дебага
    def dump(self) -> dict:
        pprint(self.state)
        return self.state
