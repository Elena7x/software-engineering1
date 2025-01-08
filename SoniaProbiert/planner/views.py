from typing import List
from planner.core import Aufgabe


class CalendarView:
    def draw_calendar(self, entries: List[Aufgabe]):
        """Zeigt alle Aufgaben in einer Kalenderähnlichen Ansicht an."""
        print("Kalenderansicht:")
        for entry in sorted(entries, key=lambda e: e.deadline):
            print(f"- {entry.deadline.strftime('%Y-%m-%d')}: {entry.name} (Priorität: {entry.priority}, Tag: {entry.tag})")

    def show_only_selected(self, entries: List[Aufgabe], priority=None, tag=None):
        """Filtert und zeigt Aufgaben basierend auf Priorität und/oder Tag."""
        filtered_entries = [
            entry for entry in entries
            if (priority is None or entry.priority == priority) and
               (tag is None or entry.tag == tag)
        ]
        self.draw_calendar(filtered_entries)


class ListView:
    def draw_list(self, entries: List[Aufgabe]):
        """Zeigt alle Aufgaben in einer tabellenartigen Listenansicht an."""
        print("Listenansicht:")
        print(f"{'Name':<20}{'Deadline':<15}{'Priorität':<10}{'Tag':<10}")
        print("-" * 60)
        for entry in sorted(entries, key=lambda e: e.deadline):
            print(f"{entry.name:<20}{entry.deadline.strftime('%Y-%m-%d'):<15}{entry.priority:<10}{entry.tag:<10}")

    def show_only_selected(self, entries: List[Aufgabe], priority=None, tag=None):
        """Filtert und zeigt Aufgaben basierend auf Priorität und/oder Tag."""
        filtered_entries = [
            entry for entry in entries
            if (priority is None or entry.priority == priority) and
               (tag is None or entry.tag == tag)
        ]
        self.draw_list(filtered_entries)
