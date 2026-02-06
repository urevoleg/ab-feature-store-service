from triggers.dsl import match_where


class TriggerEngine:
    def __init__(self, triggers, store):
        self.triggers = triggers
        self.store = store

    def process(self, event):
        for trigger in self.triggers:
            if not match_where(trigger.where, event.props):
                continue

            if trigger.type == "flag":
                self.store.set_flag_once(event.user_id, trigger.name, event.ts)

            elif trigger.type == "metric":
                self.store.inc_metric(event.user_id, trigger.name, event.ts)
