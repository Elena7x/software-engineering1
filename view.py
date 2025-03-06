import tkinter as tk

class StudyMasterPlannerView:
    # Hier wird Ansicht für mögliche Aktionen angezeigt
    def __init__(self, root):
        self.root = root
        self.root.title("Study Master Planner")

        # Hauptlayout-Frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        """ Erstellt Buttons, um zwischen den Ansichten zu wechseln """
        button_frame = tk.Frame(self.main_frame, height=200)  # Feste Höhe für Sichtbarkeit
        button_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Aufgaben-Button (nimmt 30% der Breite ein, unterhalb des ersten Buttons)
        btn_tasks = tk.Button(button_frame, text="Aufgaben hinzufügen", command=self.show_task_input)
        btn_tasks.place(relx=0.5, rely=0.1, relwidth=0.5, anchor="center")  # 30% der Breite, zentriert

        # Kalender-Button (nimmt 30% der Breite ein, zentriert)
        btn_calendar = tk.Button(button_frame, text="Kalender anzeigen", command=lambda: print("Kalender-Button geklickt!"))
        btn_calendar.place(relx=0.5, rely=0.2, relwidth=0.5, anchor="center")  # 30% der Breite, zentriert

        btn_list = tk.Button(button_frame, text="Liste anzeigen",command=lambda: print("Liste-Button geklickt!"))
        btn_list.place(relx=0.5, rely=0.3, relwidth=0.5, anchor="center")

    def show_task_input(self):
        """ Öffnet die Eingabemaske für eine neue Aufgabe """
        Task(self.root)  # Erstellt das Fenster

class Task:
    def __init__(self, parent):
        """ Erstellt eine Eingabemaske für neue Aufgaben """
        self.top = tk.Toplevel(parent)  # Neues Fenster (Modal)
        self.top.title("Neue Aufgabe hinzufügen")

        # Label und Eingabefeld für Aufgabenname
        tk.Label(self.top, text="Aufgabe:").pack(pady=5)
        self.task_entry = tk.Entry(self.top, width=40)
        self.task_entry.pack(pady=5)

        tk.Label(self.top, text="Tag:").pack(pady=5)
        self.tag_entry = tk.Entry(self.top, width=40)
        self.tag_entry.pack(pady=5)

        # Buttons für Speichern und Abbrechen
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=10)

        btn_save = tk.Button(button_frame, text="Speichern")
        btn_save.pack(side=tk.LEFT, padx=10)

        btn_cancel = tk.Button(button_frame, text="Abbrechen", command=lambda: print("Abgebrochen"))
        btn_cancel.pack(side=tk.RIGHT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()  # Erstelle das Hauptfenster
    app = StudyMasterPlannerView(root)  # Initialisiere die Klasse
    root.mainloop()  # Starte das Tkinter-Event-Loop

