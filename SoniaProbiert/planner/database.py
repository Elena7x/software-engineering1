import json
from datetime import datetime
from planner.models import Aufgabe




class Database:
    def __init__(self, file_path="tasks.json", categories_path="categories.json"):
        self.file_path = file_path
        self.categories_path = categories_path
        self.entries = {}
        self.categories = ["DHBW", "Persönliche Aufgaben"]
        self.load_data()
        self.load_categories()

    def save_entry(self, entry: Aufgabe):
        """Speichert eine neue Aufgabe in der Datenbank."""
        self.entries[entry.name] = {
            "name": entry.name,
            "deadline": entry.deadline.strftime("%Y-%m-%d"),
            "priority": entry.priority,
            "category": entry.category,
            "text": entry.text,
            "links": entry.links,  # Speichern der Anhänge
            "reminder": entry.reminder.time.strftime("%Y-%m-%d %H:%M:%S") if entry.reminder else None
        }
        self.save_data()



    def remove_entry(self, name: str):
        """Entfernt eine Aufgabe aus der Datenbank."""
        if name in self.entries:
            del self.entries[name]
            self.save_data()
        else:
            raise ValueError(f"Aufgabe mit dem Namen '{name}' existiert nicht.")

    def get_all_entries(self):
        """Gibt alle Aufgaben als Liste von `Aufgabe`-Objekten zurück."""
        return [
            Aufgabe(
                name=data["name"],
                deadline=datetime.strptime(data["deadline"], "%Y-%m-%d"),
                priority=data["priority"],
                category=data.get("category", "Allgemein"),  # Standardkategorie verwenden
                text=data.get("text", ""),
                links=data.get("links", [])  # Anhänge laden
            ) for data in self.entries.values()
        ]


    def check_name_exists(self, name: str) -> bool:
        """Prüft, ob eine Aufgabe mit dem Namen existiert."""
        return name in self.entries

    def load_data(self):
        """Lädt Daten aus der JSON-Datei."""
        try:
            with open(self.file_path, "r") as file:
                self.entries = json.load(file)
            print("Daten aus der Datei geladen:", self.entries) 
        except FileNotFoundError:
            self.entries = {}
        except json.JSONDecodeError:
            print("Fehler beim Laden der Datenbank. Datei ist beschädigt.")
            self.entries = {}

    def save_data(self):
        """Speichert die aktuellen Daten in die JSON-Datei."""
        with open(self.file_path, "w") as file:
            json.dump(self.entries, file, indent=4)

    def load_categories(self):
        """Lädt Kategorien aus der JSON-Datei."""
        try:
            with open(self.categories_path, "r") as file:
                self.categories = json.load(file)
        except FileNotFoundError:
            self.save_categories()
        except json.JSONDecodeError:
            print("Fehler beim Laden der Kategorien. Datei ist beschädigt.")
            self.categories = ["DHBW", "Persönliche Aufgaben"]
            
    def save_categories(self):
        """Speichert die Kategorien in einer JSON-Datei."""
        with open(self.categories_path, "w") as file:
            json.dump(self.categories, file, indent=4)