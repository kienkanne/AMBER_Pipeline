import json
from pathlib import Path


class RunState:
    """
    Simple checkpoint state for resume support.
    """

    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if self.path.exists():
            self.state = self.load()
        else:
            self.state = {}

    def load(self):
        with open(self.path) as f:
            return json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def mark_done(self, stage):
        self.state[stage] = "done"
        self.save()

    def mark_running(self, stage):
        self.state[stage] = "running"
        self.save()

    def mark_failed(self, stage):
        self.state[stage] = "failed"
        self.save()

    def is_done(self, stage):
        return self.state.get(stage) == "done"