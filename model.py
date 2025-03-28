import json
class Task:
    """
    eine einzelne Aufgabe 
    """
    def __init__(self, name, deadline):
        self.name = name
        self.deadline = deadline

    def __str__(self):
        return f"Task(name='{self.name}', deadline='{self.deadline}')"


class StudyMasterPlaner:
    """
    Verwalten aller Aufgaben. 
    """
    def __init__(self):
        # Liste aller Tasks
        self.tasks = []
        self.load_from_json("tasks.json")  # automatisch laden

    def create_entry(self, name, deadline):
        """
        Erstellt eine neue Task und fügt ihn der Liste hinzu.
        """
        new_task = Task(name, deadline)
        self.tasks.append(new_task)
        return new_task

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

    def edit_entries(self, old_name, new_name=None, new_deadline=None):
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
            with open(filename, "r") as f:
                data = json.load(f)
                for task_data in data.values():
                    name = task_data.get("name")
                    deadline = task_data.get("deadline")
                    if name and deadline:
                        self.tasks.append(Task(name, deadline))
        except Exception as e:
            print(f"[Fehler beim Laden]: {e}")

