import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from planner.core import StudyMasterPlaner

class StudyMasterPlanerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Master Planer")
        self.planner = StudyMasterPlaner()

        # Hauptlayout
        self.create_menu()
        self.create_task_input_section()
        self.create_task_view()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Datei-Menü
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Beenden", command=self.root.quit)

        # Ansicht-Menü
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ansicht", menu=view_menu)
        view_menu.add_command(label="Kalenderansicht", command=self.show_calendar_view)
        view_menu.add_command(label="Listenansicht", command=self.show_list_view)

    def create_task_input_section(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=10, fill="x")

        # Eingabefelder für neue Aufgaben
        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.deadline_entry = tk.Entry(frame)
        self.deadline_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Priorität:").grid(row=2, column=0, padx=5, pady=5)
        self.priority_entry = tk.Entry(frame)
        self.priority_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Tag:").grid(row=3, column=0, padx=5, pady=5)
        self.tag_entry = tk.Entry(frame)
        self.tag_entry.grid(row=3, column=1, padx=5, pady=5)

        # Button zum Hinzufügen von Aufgaben
        add_button = tk.Button(frame, text="Aufgabe hinzufügen", command=self.add_task)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_task_view(self):
        # Aufgabenansicht (z. B. Treeview für Tabellenansicht)
        self.tree = Treeview(self.root, columns=("Deadline", "Priorität", "Tag"), show="headings")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priorität", text="Priorität")
        self.tree.heading("Tag", text="Tag")
        self.tree.pack(pady=10, fill="both", expand=True)

    def add_task(self):
        try:
            name = self.name_entry.get()
            deadline = datetime.strptime(self.deadline_entry.get(), "%Y-%m-%d")
            priority = int(self.priority_entry.get())
            tag = self.tag_entry.get()

            # Neue Aufgabe erstellen
            self.planner.create_entry(name, deadline, priority, tag)
            self.refresh_task_view()
            messagebox.showinfo("Erfolg", "Aufgabe hinzugefügt!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def refresh_task_view(self):
        # Aktuelle Aufgaben in der Treeview anzeigen
        for i in self.tree.get_children():
            self.tree.delete(i)

        for task in self.planner.load_entries():
            self.tree.insert("", "end", values=(task.deadline.strftime("%Y-%m-%d"), task.priority, task.tag))

    def show_calendar_view(self):
        # Dummy-Methode für Kalenderansicht (kann angepasst werden)
        messagebox.showinfo("Kalenderansicht", "Kalenderansicht wird hier angezeigt!")

    def show_list_view(self):
        # Dummy-Methode für Listenansicht (aktuell aktualisiert sie nur die Ansicht)
        self.refresh_task_view()


# Hauptprogramm starten
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyMasterPlanerUI(root)
    root.mainloop()
