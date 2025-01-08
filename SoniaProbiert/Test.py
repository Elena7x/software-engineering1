from datetime import datetime
from typing import List

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
            raise ValueError(f"Field {field} does not exist.")

    def set_reminder(self, time: datetime):
        self.reminder = Reminder(self.name, time)


class Reminder:
    def __init__(self, name: str, time: datetime):
        self.name = name
        self.time = time


class CalendarView:
    def draw_calendar(self, entries: List[Aufgabe]):
        # Simple representation of calendar view
        print("Calendar View:")
        for entry in entries:
            print(f"{entry.name} - {entry.deadline.strftime('%Y-%m-%d')}")

    def show_only_selected(self, entries: List[Aufgabe], priority=None, tag=None):
        filtered_entries = [entry for entry in entries if (priority is None or entry.priority == priority) and
                            (tag is None or entry.tag == tag)]
        self.draw_calendar(filtered_entries)


class ListView:
    def draw_list(self, entries: List[Aufgabe]):
        # Simple representation of list view
        print("List View:")
        for entry in entries:
            print(f"{entry.name} - {entry.deadline.strftime('%Y-%m-%d')} - Priority: {entry.priority} - Tag: {entry.tag}")

    def show_only_selected(self, entries: List[Aufgabe], priority=None, tag=None):
        filtered_entries = [entry for entry in entries if (priority is None or entry.priority == priority) and
                            (tag is None or entry.tag == tag)]
        self.draw_list(filtered_entries)


class Database:
    def __init__(self):
        self.entries = {}

    def save_entry(self, entry: Aufgabe):
        self.entries[entry.name] = entry

    def remove_entry(self, name: str):
        if name in self.entries:
            del self.entries[name]
        else:
            raise ValueError(f"Entry {name} does not exist.")

    def get_all_entries(self) -> List[Aufgabe]:
        return list(self.entries.values())

    def check_name_exists(self, name: str) -> bool:
        return name in self.entries


class StudyMasterPlaner:
    def __init__(self):
        self.database = Database()
        self.calendar_view = CalendarView()
        self.list_view = ListView()

    def create_entry(self, name: str, deadline: datetime, priority: int = 1, tag: str = "", text: str = ""):
        if self.database.check_name_exists(name):
            raise ValueError(f"Entry with name {name} already exists.")
        new_entry = Aufgabe(name, deadline, priority, tag, text)
        self.database.save_entry(new_entry)

    def delete_entry(self, name: str):
        self.database.remove_entry(name)

    def edit_entry(self, name: str, field: str, new_value):
        if not self.database.check_name_exists(name):
            raise ValueError(f"Entry {name} does not exist.")
        entry = self.database.entries[name]
        entry.change_value(field, new_value)

    def load_entries(self):
        return self.database.get_all_entries()

    def show_calendar_view(self):
        entries = self.database.get_all_entries()
        self.calendar_view.draw_calendar(entries)

    def show_list_view(self):
        entries = self.database.get_all_entries()
        self.list_view.draw_list(entries)

    def filter_calendar_view(self, priority=None, tag=None):
        entries = self.database.get_all_entries()
        self.calendar_view.show_only_selected(entries, priority, tag)

    def filter_list_view(self, priority=None, tag=None):
        entries = self.database.get_all_entries()
        self.list_view.show_only_selected(entries, priority, tag)

if __name__ == "__main__":
    planner = StudyMasterPlaner()
    
    # Aufgaben erstellen
    planner.create_entry("Aufgabe 1", datetime(2025, 1, 10), priority=2, tag="Wichtig", text="Lernen für Prüfung")
    planner.create_entry("Aufgabe 2", datetime(2025, 1, 15), priority=1, tag="Normal", text="Hausaufgaben")
    
    # Kalenderansicht anzeigen
    print("\n--- Kalenderansicht ---")
    planner.show_calendar_view()

    # Listenansicht anzeigen
    print("\n--- Listenansicht ---")
    planner.show_list_view()

    # Gefilterte Kalenderansicht
    print("\n--- Gefilterte Kalenderansicht (Priority: 2) ---")
    planner.filter_calendar_view(priority=2)

    # Aufgabe bearbeiten
    print("\n--- Aufgabe bearbeiten ---")
    planner.edit_entry("Aufgabe 1", "priority", 1)
    planner.show_list_view()

    # Reminder hinzufügen
    print("\n--- Reminder hinzufügen ---")
    planner.database.entries["Aufgabe 1"].set_reminder(datetime(2025, 1, 9))
    print(f"Reminder gesetzt: {planner.database.entries['Aufgabe 1'].reminder.time}")

    # Aufgabe löschen
    print("\n--- Aufgabe löschen ---")
    planner.delete_entry("Aufgabe 2")
    planner.show_list_view()
