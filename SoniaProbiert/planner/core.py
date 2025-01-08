from datetime import datetime
from typing import List
from planner.database import Database

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
        """Ändert den Wert eines Attributs, wenn es existiert."""
        if hasattr(self, field):
            setattr(self, field, new_value)
        else:
            raise ValueError(f"Field '{field}' does not exist in Aufgabe.")

    def set_reminder(self, time: datetime):
        """Setzt eine Erinnerung für die Aufgabe."""
        self.reminder = Reminder(self.name, time)

    def __repr__(self):
        return f"<Aufgabe(name={self.name}, deadline={self.deadline}, priority={self.priority}, tag={self.tag})>"


class Reminder:
    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time

    def update_time(self, new_time: datetime):
        """Aktualisiert die Zeit des Reminders."""
        self.time = new_time

    def __repr__(self):
        return f"<Reminder(name={self.name}, time={self.time})>"


class StudyMasterPlaner:
    def __init__(self):
        """Initialisiert den Planer mit einer leeren Liste von Aufgaben."""
        self.entries = {}
        self.database = Database()  # Initialisierung der Datenbank

    def create_entry(self, name: str, deadline: datetime, priority: int = 1, tag: str = "", text: str = ""):
        """Erstellt eine neue Aufgabe."""
        if name in self.entries:
            raise ValueError(f"Eine Aufgabe mit dem Namen '{name}' existiert bereits.")
        new_task = Aufgabe(name, deadline, priority, tag, text)
        self.entries[name] = new_task

    def delete_entry(self, name: str):
        """Löscht eine Aufgabe nach ihrem Namen."""
        if name in self.entries:
            del self.entries[name]
        else:
            raise ValueError(f"Keine Aufgabe mit dem Namen '{name}' gefunden.")

    def edit_entry(self, name: str, field: str, new_value):
        """Bearbeitet ein Feld einer existierenden Aufgabe."""
        if name not in self.entries:
            raise ValueError(f"Keine Aufgabe mit dem Namen '{name}' gefunden.")
        entry = self.entries[name]
        entry.change_value(field, new_value)
        
    def load_entries(self):
        """Lädt alle Aufgaben aus der Datenbank."""
        return self.database.get_all_entries()

    def set_reminder(self, name: str, time: datetime):
        """Setzt einen Reminder für eine Aufgabe."""
        if name not in self.entries:
            raise ValueError(f"Keine Aufgabe mit dem Namen '{name}' gefunden.")
        self.entries[name].set_reminder(time)

    def get_all_entries(self) -> List[Aufgabe]:
        """Gibt alle Aufgaben zurück."""
        return list(self.entries.values())

    def filter_entries(self, priority: int = None, tag: str = None) -> List[Aufgabe]:
        """Filtert Aufgaben nach Priorität und/oder Tag."""
        return [
            entry for entry in self.entries.values()
            if (priority is None or entry.priority == priority) and
               (tag is None or entry.tag == tag)
        ]

    def __repr__(self):
        return f"<StudyMasterPlaner(entries={len(self.entries)})>"
