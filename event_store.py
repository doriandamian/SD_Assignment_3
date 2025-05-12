from events import *
import json

class EventStore:
    def __init__(self, filename: str = "event_log.jsonl"):
        self.filename = filename

    def append(self, event: Event):
        with open(self.filename, "a") as log:
            log.write(json.dumps(event.to_dict()) + "\n")

    def get_all_events(self):
        events = []
        try:
            with open(self.filename, "r") as log:
                for line in log:
                    data = json.loads(line.strip())
                    events.append(Event.from_dict(data))
        except FileNotFoundError:
            pass
        return events