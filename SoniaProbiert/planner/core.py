from datetime import datetime
from typing import List
from planner.database import Database
from planner.models import Aufgabe, Reminder


class Aufgabe:
    def __init__(self, name: str, deadline: datetime, priority: int = 1, category: str = "", text: str = ""):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.category = category
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


class StudyMasterPlaner:
    def __init__(self):
        """Initialisiert den Planer mit einer leeren Liste von Aufgaben."""
        self.database = Database()  # Initialisierung der Datenbank
        self.entries = {}
        
    def create_entry(self, name: str, deadline: datetime, priority: int = 1, category: str = "Allgemein", text: str = ""):
        if self.database.check_name_exists(name):
            raise ValueError(f"Eine Aufgabe mit dem Namen '{name}' existiert bereits.")
        new_task = Aufgabe(name, deadline, priority, category, text)
        self.database.save_entry(new_task)

    def delete_entry(self, name: str):
        """Löscht eine Aufgabe nach ihrem Namen."""
        self.database.remove_entry(name)
    
    def edit_entry(self, name: str, field: str, new_value):
        """Bearbeitet ein Feld einer existierenden Aufgabe."""
        tasks = self.database.get_all_entries()
        for task in tasks:
            if task.name == name:
                task.change_value(field, new_value)
                self.database.save_entry(task)
                return
        raise ValueError(f"Keine Aufgabe mit dem Namen '{name}' gefunden.")
        
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

    def filter_entries(self, priority: int = None, category: str = None) -> List[Aufgabe]:
        """Filtert Aufgaben nach Priorität und/oder category."""
        return [
            entry for entry in self.entries.values()
            if (priority is None or entry.priority == priority) and
               (category is None or entry. category == category)
        ]

    def __repr__(self):
        return f"<StudyMasterPlaner(entries={len(self.entries)})>"
