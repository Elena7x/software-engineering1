import json

from scripts.regsetup import description


class Task:
    """
    eine einzelne Aufgabe 
    """
    def __init__(self, name, deadline, priority, category, description, reminder):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.category = category
        self.description = description
        self.reminder = reminder

    def __str__(self):
        return f"Task(name='{self.name}', deadline='{self.deadline}', priority={self.priority}, category='{self.category}, description={self.description}, reminder={self.reminder})')"


class StudyMasterPlaner:
    """
    Verwalten aller Aufgaben. 
    """
    def __init__(self):
        # Liste aller Tasks
        self.tasks = []
        self.load_from_json("tasks.json")  # automatisch laden

    def create_entry(self, name, deadline, priority, category, description, reminder):
        """
        Erstellt eine neue Task und fügt ihn der Liste hinzu.
        """
        if not name:
            return {"status": "error", "message": "Ungültige Eingabe: Name fehlt"}
        new_task = Task(name, deadline, priority, category, description, reminder)
        self.tasks.append(new_task)
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump([task.__dict__ for task in self.tasks], f, ensure_ascii=False, indent=4)
        return {"status": "info", "message": "Aufgabe erfolgreich angelegt"}


    def delete_entry(self, name):
        """
        Löscht einen Task anhand des Namens aus der Liste.
        Gibt True zurück, wenn ein Task gelöscht wurde,
        sonst False.
        """
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)
                return True
        return False

    def edit_entries(self, old_name, new_name=None, new_deadline=None, new_priority=None, new_category=None, new_description=None, new_reminder=None):
        """
        Bearbeitet einen bestehenden Task. Sucht anhand des alten Namens.
        Optional können neuer Name und/oder neues Fälligkeitsdatum
        übergeben werden. Gibt True zurück, wenn etwas bearbeitet wurde,
        sonst False.
        """
        for task in self.tasks:
            if task.name == old_name:
                if new_name:
                    task.name = new_name
                if new_deadline:
                    task.deadline = new_deadline
                if new_priority:
                    task.priority = new_priority
                if new_category:
                    task.category = new_category
                if new_description:
                    task.description = new_description
                if new_reminder:
                    task.reminder = new_reminder
                return True
        return False

    def load_entry(self, name):
        """
        Lädt einen Task anhand des Namens aus der Liste.
        Gibt das Task-Objekt zurück oder None, falls kein Task
        gefunden wird.
        """
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def load_from_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for task_data in data:
                    name = task_data.get("name")
                    deadline = task_data.get("deadline")
                    priority = task_data.get("priority")
                    category = task_data.get("category")
                    description = task_data.get("description")
                    reminder = task_data.get("reminder")

                    if name and deadline:
                        self.tasks.append(Task(name, deadline, priority, category, description, reminder))
        except Exception as e:
            print(f"[Fehler beim Laden]: {e}")

    def save_to_json(self, filename="tasks.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([task.__dict__ for task in self.tasks], f, ensure_ascii=False, indent=4)
            
    


