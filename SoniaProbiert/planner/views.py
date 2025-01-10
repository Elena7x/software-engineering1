from typing import List
from planner.models import Aufgabe

class CalendarView:
    def draw_calendar(self, entries: List[Aufgabe]):
        """Zeigt alle Aufgaben in einer Kalenderähnlichen Ansicht an."""
        print("Kalenderansicht:")
        for entry in sorted(entries, key=lambda e: e.deadline):
            print(f"- {entry.deadline.strftime('%Y-%m-%d')}: {entry.name} (Priorität: {entry.priority})")

    def show_only_selected(self, entries: List[Aufgabe], priority=None, category=None):
        """Filtert und zeigt Aufgaben basierend auf Priorität und/oder Kategorie."""
        filtered_entries = [
            entry for entry in entries
            if (priority is None or entry.priority == priority) and
               (category is None or entry.category == category)
        ]
        self.draw_calendar(filtered_entries)

class ListView:
    def draw_list(self, entries: List[Aufgabe]):
        """Zeigt alle Aufgaben in einer tabellenartigen Listenansicht an."""
        print("Listenansicht:")
        print(f"{'Name':<20}{'Deadline':<15}{'Priorität':<10}{'Kategorie':<10}")
        print("-" * 60)
        for entry in sorted(entries, key=lambda e: e.deadline):
            print(f"{entry.name:<20}{entry.deadline.strftime('%Y-%m-%d'):<15}{entry.priority:<10}{entry.category:<10}")

    def show_only_selected(self, entries: List[Aufgabe], priority=None, category=None):
        """Filtert und zeigt Aufgaben basierend auf Priorität und/oder Kategorie."""
        filtered_entries = [
            entry for entry in entries
            if (priority is None or entry.priority == priority) and
               (category is None or entry.category == category)
        ]
        self.draw_list(filtered_entries)
