from collections import defaultdict
from datetime import datetime, date
from typing import List

from state.store import StateStore
from state.models import TriggerState


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

    def _date_str(self, ts: datetime) -> str:
        return ts.strftime("%Y-%m-%d")

    def _date(self, ts: datetime) -> date:
        return ts.date()

    def set_flag_once(self, user_id: str, name: str, ts: datetime):
        date_key = self._date_str(ts)
        self.state[date_key][user_id]["flags"].add(name)

    def inc_metric(self, user_id: str, name: str, ts: datetime):
        date_key = self._date_str(ts)
        self.state[date_key][user_id]["metrics"][name] += 1

    def dump(self) -> List[TriggerState]:
        """
        Возвращает массив TriggerState (Pydantic),
        готовых к сериализации и отправке
        """
        result: List[TriggerState] = []

        for date_str, users in self.state.items():
            d = date.fromisoformat(date_str)

            for user_id, payload in users.items():
                result.append(
                    TriggerState(
                        date=d,
                        user_id=user_id,
                        flags=sorted(payload["flags"]),
                        metrics=dict(payload["metrics"]),
                    )
                )

        return result

    def clear(self):
        """
        Очистка стора (например, после успешной отправки в Kafka)
        """
        self.state.clear()
