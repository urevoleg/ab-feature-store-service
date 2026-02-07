from triggers.dsl.trigger import match_trigger
from triggers.dsl.event_name import match_event_name


class TriggerEngine:
    def __init__(self, triggers, store):
        self.triggers = triggers
        self.store = store

    def process(self, event):
        for trigger in self.triggers:

            # 1️ event_name DSL
            if not match_event_name(trigger.event_name, event.event_name):
                continue

            # 2️ where DSL (event_attrs)
            if not match_trigger(trigger.where, event.props):
                continue

            # 3️apply trigger
            if trigger.type == "flag":
                self.store.set_flag_once(
                    event.user_id, trigger.name, event.ts
                )

            elif trigger.type == "metric":
                self.store.inc_metric(
                    event.user_id, trigger.name, event.ts
                )
