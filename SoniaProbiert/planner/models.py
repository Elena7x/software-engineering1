from datetime import datetime

class Aufgabe:
    def __init__(self, name, deadline, priority, category, text="", links=None, reminder=None):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.category = category
        self.text = text
        self.links = links if links is not None else []  # Standardmäßig eine leere Liste
        self.reminder = reminder


    def change_value(self, field: str, new_value):
        """Ändert den Wert eines Attributs der Aufgabe."""
        if hasattr(self, field):
            setattr(self, field, new_value)
        else:
            raise ValueError(f"Das Feld '{field}' existiert nicht.")
        
    def set_reminder(self, time: datetime):
        self.reminder = Reminder(self.name, time)

    def __repr__(self):
        return f"<Aufgabe(name={self.name}, deadline={self.deadline}, priority={self.priority}, category={self.category})>"


class Reminder:
    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time

    def update_time(self, new_time: datetime):
        self.time = new_time

    def __repr__(self):
        return f"<Reminder(name={self.name}, time={self.time})>"
