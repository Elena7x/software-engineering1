import tkinter as tk

class StudyMasterPlannerView:
    # Hier wird Ansicht für mögliche Aktionen angezeigt
    def __init__(self, root):
        self.root = root
        self.root.title("Study Master Planner")

        # Menü erstellen
        #self.create_menu()

        # Hauptlayout-Frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_navigation_buttons()

        # Aufgaben-Eingabebereich
        #self.create_task_input_section(self.main_frame)

        # Aufgaben-Anzeige
        #self.create_task_view(self.main_frame)

    def create_navigation_buttons(self):
        """ Erstellt Buttons, um zwischen den Ansichten zu wechseln """
        button_frame = tk.Frame(self.main_frame, height=200)  # Feste Höhe für Sichtbarkeit
        button_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Aufgaben-Button (nimmt 30% der Breite ein, unterhalb des ersten Buttons)
        btn_tasks = tk.Button(button_frame, text="Aufgaben anzeigen", command=lambda: print("Aufgaben-Button geklickt!"))
        btn_tasks.place(relx=0.5, rely=0.1, relwidth=0.5, anchor="center")  # 30% der Breite, zentriert

        # Kalender-Button (nimmt 30% der Breite ein, zentriert)
        btn_calendar = tk.Button(button_frame, text="Kalender anzeigen", command=lambda: print("Kalender-Button geklickt!"))
        btn_calendar.place(relx=0.5, rely=0.2, relwidth=0.5, anchor="center")  # 30% der Breite, zentriert

        btn_list = tk.Button(button_frame, text="Liste anzeigen",command=lambda: print("Liste-Button geklickt!"))
        btn_list.place(relx=0.5, rely=0.3, relwidth=0.5, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()  # Erstelle das Hauptfenster
    app = StudyMasterPlannerView(root)  # Initialisiere die Klasse
    root.mainloop()  # Starte das Tkinter-Event-Loop

