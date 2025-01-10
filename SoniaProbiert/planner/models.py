from datetime import datetime

class Aufgabe:
    def __init__(self, name: str, deadline: datetime, priority: int = 1, category: str = "", text: str = ""):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.category = category
        self.text = text
        self.reminder = None

    def change_value(self, field: str, new_value):
        """Ändert den Wert eines Attributs, wenn es existiert."""
        if hasattr(self, field):
            setattr(self, field, new_value)
        else:
            raise ValueError(f"Field '{field}' does not exist in Aufgabe.")

    def set_reminder(self, time: datetime):
        """Setzt eine Erinnerung für die Aufgabe."""
        self.reminder = Reminder(self.name, time)

    def __repr__(self):
        return f"<Aufgabe(name={self.name}, deadline={self.deadline}, priority={self.priority}, category={self.category})>"

class Reminder:
    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time

    def update_time(self, new_time: datetime):
        """Aktualisiert die Zeit des Reminders."""
        self.time = new_time

    def __repr__(self):
        return f"<Reminder(name={self.name}, time={self.time})>"
