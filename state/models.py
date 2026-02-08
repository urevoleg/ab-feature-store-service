from datetime import date
from typing import Dict, List
import pendulum
from pydantic import BaseModel, Field


class TriggerMetrics(BaseModel):
    name: str
    value: int


class TriggerState(BaseModel):
    """
    Состояние пользователя за день
    """
    date: date
    user_id: str

    flags: List[str] = Field(default_factory=list)
    metrics: Dict[str, int] = Field(default_factory=dict)

    timestamp: int = Field(default_factory=pendulum.now("UTC").timestamp)

    def __repr__(self) -> str:
        flags = ", ".join(sorted(self.flags)) if self.flags else "—"
        metrics = (
            ", ".join(f"{k}={v}" for k, v in sorted(self.metrics.items()))
            if self.metrics
            else "—"
        )

        return (
            "TriggerState("
            f"📅 date={self.date}\n"
            f"🧍‍♂️ user_id={self.user_id}\n"
            f"🚩 flags=[{flags}]\n"
            f"🪫 metrics={{ {metrics} }})\n"
            f" now: {pendulum.from_timestamp(self.timestamp, "local")}\n"
        )