from datetime import datetime

class Aufgabe:
    def __init__(self, name: str, deadline: datetime, priority: int = 1, tag: str = "", text: str = ""):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.tag = tag
        self.text = text
        self.links = []
        self.reminder = None

    def change_value(self, field: str, new_value):
        if hasattr(self, field):
            setattr(self, field, new_value)
        else:
            raise ValueError(f"Field '{field}' does not exist in Aufgabe.")

    def set_reminder(self, time: datetime):
        self.reminder = Reminder(self.name, time)

    def __repr__(self):
        return f"<Aufgabe(name={self.name}, deadline={self.deadline}, priority={self.priority}, tag={self.tag})>"


class Reminder:
    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time

    def update_time(self, new_time: datetime):
        self.time = new_time

    def __repr__(self):
        return f"<Reminder(name={self.name}, time={self.time})>"
