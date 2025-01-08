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
        
        self.refresh_task_view()

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
        
        # Button zum Speichern der Änderungen
        save_button = tk.Button(frame, text="Änderungen speichern", command=self.update_task)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def create_task_view(self):
        """Erstellt die Treeview zur Anzeige der Aufgaben."""
        # Treeview konfigurieren
        self.tree = Treeview(self.root, columns=("Name", "Deadline", "Priorität", "Tag"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priorität", text="Priorität")
        self.tree.heading("Tag", text="Tag")

        # Spaltenbreite anpassen (optional)
        self.tree.column("Name", width=200)
        self.tree.column("Deadline", width=100)
        self.tree.column("Priorität", width=80)
        self.tree.column("Tag", width=100)

        # Treeview packen
        self.tree.pack(pady=10, fill="both", expand=True)
        
        # Bind Treeview-Auswahl an Methode
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def add_task(self):
        """Fügt eine neue Aufgabe hinzu und aktualisiert die Anzeige."""
        try:
            # Eingaben aus den Feldern lesen
            name = self.name_entry.get()
            deadline = datetime.strptime(self.deadline_entry.get(), "%Y-%m-%d")
            priority = int(self.priority_entry.get())
            tag = self.tag_entry.get()

            # Aufgabe erstellen
            self.planner.create_entry(name, deadline, priority, tag)

            # Aktualisiere die Treeview
            self.refresh_task_view()

            # Eingabefelder leeren
            self.name_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.tag_entry.delete(0, tk.END)

            messagebox.showinfo("Erfolg", "Aufgabe erfolgreich hinzugefügt!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            
    def update_task(self):
        """Speichert die geänderten Daten der ausgewählten Aufgabe."""
        try:
            # Hole den ausgewählten Aufgaben-Namen
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Fehler", "Bitte eine Aufgabe auswählen!")
                return

            old_name = self.tree.item(selected_item[0], "values")[0]  # Name der Aufgabe vor Änderung

            # Werte aus den Eingabefeldern lesen
            new_name = self.name_entry.get()
            new_deadline = datetime.strptime(self.deadline_entry.get(), "%Y-%m-%d")
            new_priority = int(self.priority_entry.get())
            new_tag = self.tag_entry.get()

            # Bearbeitung der Aufgabe
            if old_name == new_name:
                # Wenn der Name nicht geändert wurde, nur die Felder aktualisieren
                self.planner.edit_entry(new_name, "deadline", new_deadline)
                self.planner.edit_entry(new_name, "priority", new_priority)
                self.planner.edit_entry(new_name, "tag", new_tag)
            else:
                # Wenn der Name geändert wurde, alte Aufgabe löschen und neue erstellen
                self.planner.delete_entry(old_name)
                self.planner.create_entry(new_name, new_deadline, new_priority, new_tag)

            # Treeview aktualisieren
            self.refresh_task_view()
            messagebox.showinfo("Erfolg", "Aufgabe erfolgreich aktualisiert!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def refresh_task_view(self):
        """Aktualisiert die Treeview mit den aktuellen Aufgaben."""
        # Lösche alle vorhandenen Einträge in der Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lade die Aufgaben aus dem Planer
        for task in self.planner.load_entries():
            # Füge jede Aufgabe als Zeile in die Treeview ein
            self.tree.insert(
                "", "end", 
                values=(
                    task.name, 
                    task.deadline.strftime("%Y-%m-%d"), 
                    task.priority, 
                    task.tag
                )
            )

    def on_treeview_select(self, event):
        """Lädt die ausgewählten Aufgaben-Daten in die Eingabefelder."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Hole die Werte aus der Treeview
        item = self.tree.item(selected_item[0], "values")
        name, deadline, priority, tag = item

        # Werte in die Eingabefelder einfügen
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, deadline)

        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, priority)

        self.tag_entry.delete(0, tk.END)
        self.tag_entry.insert(0, tag)


    def show_calendar_view(self):
        # Dummy-Methode für Kalenderansicht (kann angepasst werden)
        messagebox.showinfo("Kalenderansicht", "Kalenderansicht wird hier angezeigt!")

    def show_list_view(self):
        # Dummy-Methode für Listenansicht (aktuell aktualisiert sie nur die Ansicht)
        self.refresh_task_view()

    def delete_task(self):
        """Löscht die ausgewählte Aufgabe und aktualisiert die Anzeige."""
        try:
            # Ausgewählte Aufgabe in der Treeview abrufen
            selected_item = self.tree.selection()[0]  # ID der ausgewählten Zeile
            task_name = self.tree.item(selected_item, "values")[0]  # Name der Aufgabe

            # Aufgabe aus dem Planer löschen
            self.planner.delete_entry(task_name)

            # Treeview aktualisieren
            self.refresh_task_view()

            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", f"Aufgabe '{task_name}' wurde gelöscht!")
        except IndexError:
            messagebox.showerror("Fehler", "Bitte eine Aufgabe auswählen!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

# Hauptprogramm starten
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyMasterPlanerUI(root)
    root.mainloop()
