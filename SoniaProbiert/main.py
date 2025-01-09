import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter import simpledialog
from datetime import datetime
from tkcalendar import Calendar
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from planner.core import StudyMasterPlaner

class StudyMasterPlanerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Master")
        self.root.geometry("900x600")  # Fenstergröße setzen
        self.planner = StudyMasterPlaner()

        # Kategorien laden
        self.categories = self.planner.database.categories

        # Mapping für Prioritäten (numerisch zu textuell)
        self.priority_display_mapping = {
            1: "Sehr Niedrig",
            2: "Niedrig",
            3: "Hoch",
            4: "Sehr Hoch"
        }
        self.priority_reverse_mapping = {v: k for k, v in self.priority_display_mapping.items()}

        # Frames erstellen
        self.task_input_frame = tk.Frame(self.root)  # Frame für "Aufgaben Hinzufügen"
        self.task_view_frame = tk.Frame(self.root)  # Frame für die Aufgabenliste

        # Liste und Eingabemaske erstellen
        self.create_task_view(self.task_view_frame)
        self.create_task_input_section(self.task_input_frame)

        # Standardansicht: Aufgabenliste anzeigen, Eingabemaske ausblenden
        self.task_view_frame.pack(fill="both", expand=True)
        self.task_input_frame.pack_forget()

        # Aufgabenliste aktualisieren
        self.refresh_task_view()

        # Menü erstellen
        self.create_menu()



    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        # Ansicht-Menü
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_command(label="Aufgaben Hinzufügen", command=self.show_task_input)
        
        # Ansicht-Menü
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ansicht", menu=view_menu)
        view_menu.add_command(label="Kalenderansicht", command=self.show_calendar_view)
        view_menu.add_command(label="Listenansicht", command=self.hide_task_input)

    def create_task_input_section(self, parent_frame):
        frame = tk.Frame(parent_frame)
        frame.pack(pady=20, padx=10, fill="x")

        # Eingabefelder für neue Aufgaben
        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Deadline:").grid(row=1, column=0, padx=5, pady=5)
        self.deadline_label = tk.Label(frame, text="Kein Datum ausgewählt", bg="white", relief="sunken", width=20)
        self.deadline_label.grid(row=1, column=1, padx=5, pady=5)

        self.deadline_button = tk.Button(frame, text="Datum auswählen", command=self.open_calendar_popup)
        self.deadline_button.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(frame, text="Priorität:").grid(row=2, column=0, padx=5, pady=5)
        self.priority_values = ["Sehr Niedrig", "Niedrig", "Hoch", "Sehr Hoch"]
        self.selected_priority = tk.StringVar()
        self.selected_priority.set(self.priority_values[1])  # Standardwert: "Niedrig"
        self.priority_menu = tk.OptionMenu(frame, self.selected_priority, *self.priority_values)
        self.priority_menu.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Kategorie:").grid(row=3, column=0, padx=5, pady=5)
        self.selected_category = tk.StringVar()
        self.selected_category.set(self.categories[0])  # Standardkategorie
        self.category_menu = tk.OptionMenu(frame, self.selected_category, *self.categories)
        self.category_menu.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Dateianhänge
        tk.Label(frame, text="Anhänge:").grid(row=4, column=0, padx=5, pady=5)
        self.attachment_list = tk.Listbox(frame, height=4, width=40)
        self.attachment_list.grid(row=4, column=1, padx=5, pady=5)
        self.add_attachment_button = tk.Button(frame, text="Datei/Link hinzufügen", command=self.add_attachment)
        self.add_attachment_button.grid(row=4, column=2, padx=5, pady=5)
        self.remove_attachment_button = tk.Button(frame, text="Entfernen", command=self.remove_attachment)
        self.remove_attachment_button.grid(row=4, column=3, padx=5, pady=5)

        # Buttons unten
        button_frame = tk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=4, pady=10)

        # Button: Aufgabe hinzufügen
        self.add_button = tk.Button(button_frame, text="Aufgabe hinzufügen", command=self.add_task, width=18, height=1)
        self.add_button.pack(side=tk.LEFT, padx=10)

        # Button: Änderungen speichern
        self.save_button = tk.Button(button_frame, text="Änderungen speichern", command=self.update_task, width=18, height=1)
        self.save_button.pack(side=tk.LEFT, padx=10)
        self.save_button.pack_forget()  # Standardmäßig ausblenden

        # Button: Aufgabe löschen
        self.delete_button = tk.Button(button_frame, text="Aufgabe löschen", command=self.delete_task, width=18, height=1)
        self.delete_button.pack(side=tk.LEFT, padx=10)
        self.delete_button.pack_forget()  # Standardmäßig ausblenden

        # Button: Abbrechen
        self.cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.cancel_selection, width=18, height=1)
        self.cancel_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button.pack_forget()  # Standardmäßig ausblenden


    def create_task_view(self, parent_frame):
        """Erstellt die Aufgabenansicht mit Filter-, Sortier- und Anhangsoptionen."""
        # Frame für Filter- und Sortieroptionen
        filter_sort_frame = tk.Frame(parent_frame)
        filter_sort_frame.pack(pady=10, fill="x")

        # Filter nach Kategorie
        tk.Label(filter_sort_frame, text="Filter Kategorie:").pack(side=tk.LEFT, padx=5)
        self.filter_category = tk.StringVar()
        self.filter_category.set("Alle")  # Standardwert
        category_options = ["Alle"] + self.categories
        self.category_filter_menu = tk.OptionMenu(filter_sort_frame, self.filter_category, *category_options, command=self.apply_filters)
        self.category_filter_menu.pack(side=tk.LEFT, padx=5)

        # Filter nach Priorität
        tk.Label(filter_sort_frame, text="Filter Priorität:").pack(side=tk.LEFT, padx=5)
        self.filter_priority = tk.StringVar()
        self.filter_priority.set("Alle")  # Standardwert
        priority_options = ["Alle", "Sehr Niedrig", "Niedrig", "Hoch", "Sehr Hoch"]
        self.priority_filter_menu = tk.OptionMenu(filter_sort_frame, self.filter_priority, *priority_options, command=self.apply_filters)
        self.priority_filter_menu.pack(side=tk.LEFT, padx=5)

        # Sortierung
        tk.Label(filter_sort_frame, text="Sortieren nach:").pack(side=tk.LEFT, padx=5)
        self.sort_option = tk.StringVar()
        self.sort_option.set("Fälligkeitsdatum")  # Standardwert
        sort_options = ["Fälligkeitsdatum", "Priorität", "Name"]
        self.sort_menu = tk.OptionMenu(filter_sort_frame, self.sort_option, *sort_options, command=self.apply_filters)
        self.sort_menu.pack(side=tk.LEFT, padx=5)

        # Frame für die Aufgabenliste
        task_view_frame = tk.Frame(parent_frame)
        task_view_frame.pack(pady=10, fill="both", expand=True)

        # Treeview für die Aufgabenliste
        self.tree = Treeview(task_view_frame, columns=("Name", "Deadline", "Priorität", "category"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priorität", text="Priorität")
        self.tree.heading("category", text="Kategorie")
        self.tree.column("Name", width=200)
        self.tree.column("Deadline", width=100)
        self.tree.column("Priorität", width=80)
        self.tree.column("category", width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Auswahl in der Treeview überwachen
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Frame für Anhänge-Buttons
        attachment_button_frame = tk.Frame(parent_frame)
        attachment_button_frame.pack(pady=5)

        # Button zum Öffnen von Anhängen
        self.open_attachment_button = tk.Button(attachment_button_frame, text="Öffnen", command=self.open_attachment)
        self.open_attachment_button.pack(side=tk.LEFT, padx=5)


    def refresh_task_view(self):
        """Aktualisiert die Treeview mit den aktuellen Aufgaben."""
        tasks = self.planner.load_entries()

        # Treeview leeren
        self.tree.delete(*self.tree.get_children())

        # Aufgaben einfügen
        for task in tasks:
            priority_text = self.priority_display_mapping.get(task.priority, "Unbekannt")
            self.tree.insert(
                "", "end",
                values=(task.name, task.deadline.strftime("%Y-%m-%d"), priority_text, task.category)
            )

    def on_treeview_select(self, event):
        """Lädt die ausgewählten Aufgaben-Daten in die Eingabefelder und passt die Button-Sichtbarkeit an."""
        selected_item = self.tree.selection()
        if selected_item:
            # Wenn eine Aufgabe ausgewählt ist, zeige Speichern-, Löschen- und Abbrechen-Button
            self.add_button.pack_forget()
            self.save_button.pack(side=tk.LEFT, padx=10)
            self.delete_button.pack(side=tk.LEFT, padx=10)
            self.cancel_button.pack(side=tk.LEFT, padx=10)

            # Hole die Werte aus der Treeview
            item = self.tree.item(selected_item[0], "values")
            name, deadline, priority_text, category = item

            # Eingabefelder füllen
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.deadline_label.config(text=deadline)
            self.selected_priority.set(priority_text)
            self.selected_category.set(category)

            # Anhänge aus der Datenbank laden
            task = next((t for t in self.planner.load_entries() if t.name == name), None)
            if task:
                self.attachment_list.delete(0, tk.END)
                for attachment in task.links:
                    self.attachment_list.insert(tk.END, attachment)
        else:
            # Wenn keine Aufgabe ausgewählt ist, zeige nur den "Aufgabe Hinzufügen"-Button
            self.add_button.pack(side=tk.LEFT, padx=10)
            self.save_button.pack_forget()
            self.delete_button.pack_forget()
            self.cancel_button.pack_forget()

    def show_calendar_view(self):
        # Dummy-Methode für Kalenderansicht (kann angepasst werden)
        messagebox.showinfo("Kalenderansicht", "Kalenderansicht wird hier angezeigt!")

    def show_list_view(self):
        # Dummy-Methode für Listenansicht (aktuell aktualisiert sie nur die Ansicht)
        self.refresh_task_view()
        
    def show_task_input(self):
        """Zeigt den Bereich 'Aufgaben Hinzufügen' an."""
        self.task_input_frame.pack(fill="both", expand=True)  # Zeigt den Bereich zum Hinzufügen von Aufgaben an

    def hide_task_input(self):
        """Blendet den Bereich 'Aufgaben Hinzufügen' aus."""
        self.task_input_frame.pack_forget()  # Versteckt den Bereich zum Hinzufügen von Aufgaben

    def add_category(self):
        """Fügt eine neue Kategorie hinzu."""
        new_category = tk.simpledialog.askstring("Neue Kategorie", "Gib den Namen der neuen Kategorie ein:")
        if new_category:
            # Prüfen, ob die Kategorie (unabhängig von Groß-/Kleinschreibung) existiert
            if new_category.lower() not in [cat.lower() for cat in self.categories]:
                self.categories.append(new_category)  # Kategorie in Originalschreibweise speichern
                self.planner.database.categories = self.categories
                self.planner.database.save_categories()
                self.refresh_category_menu()
                messagebox.showinfo("Erfolg", f"Die Kategorie '{new_category}' wurde hinzugefügt!")
            else:
                messagebox.showerror("Fehler", f"Die Kategorie '{new_category}' existiert bereits (unabhängig von Groß-/Kleinschreibung).")

    def delete_category(self):
        """Löscht eine ausgewählte Kategorie."""
        selected_category = tk.simpledialog.askstring("Kategorie löschen", "Gib den Namen der Kategorie ein, die gelöscht werden soll:")
        if selected_category:
            if selected_category in self.categories:
                if selected_category not in ["DHBW", "Persönliche Aufgaben"]:  # Standardkategorien schützen
                    self.categories.remove(selected_category)
                    self.planner.database.categories = self.categories
                    self.planner.database.save_categories()
                    self.refresh_category_menu()  # Aktualisiert das Dropdown-Menü direkt
                    messagebox.showinfo("Erfolg", f"Die Kategorie '{selected_category}' wurde gelöscht!")
                else:
                    messagebox.showerror("Fehler", f"Die Kategorie '{selected_category}' kann nicht gelöscht werden.")
            else:
                messagebox.showerror("Fehler", f"Die Kategorie '{selected_category}' existiert nicht.")

    def refresh_category_menu(self):
        """Aktualisiert das Dropdown-Menü für Kategorien."""
        self.category_menu['menu'].delete(0, 'end')  # Entfernt alle vorhandenen Kategorien
        for category in self.categories:
            self.category_menu['menu'].add_command(label=category, command=tk._setit(self.selected_category, category))
        self.selected_category.set(self.categories[0])  # Setzt die Standardkategorie

    def open_calendar_popup(self):
        """Öffnet ein Popup-Fenster mit einem Kalender zur Auswahl eines Datums."""
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Datum auswählen")

        calendar = Calendar(calendar_window, date_pattern="yyyy-mm-dd")
        calendar.pack(pady=10, padx=10)

        def select_date():
            selected_date = calendar.get_date()
            self.deadline_label.config(text=selected_date)
            calendar_window.destroy()

        select_button = tk.Button(calendar_window, text="Datum auswählen", command=select_date)
        select_button.pack(pady=10)
        
    def cancel_selection(self):
        """Hebt die Auswahl in der Treeview auf und zeigt den 'Aufgabe Hinzufügen'-Modus."""
        self.tree.selection_remove(self.tree.selection())  # Auswahl in der Treeview entfernen
        self.name_entry.delete(0, tk.END)  # Eingabefelder leeren
        self.deadline_label.config(text="Kein Datum ausgewählt")
        self.selected_priority.set(self.priority_values[1])  # Priorität zurücksetzen
        self.selected_category.set(self.categories[0])  # Kategorie zurücksetzen
        self.attachment_list.delete(0, tk.END)  # Anhänge zurücksetzen

        # Buttons aktualisieren
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.save_button.pack_forget()
        self.delete_button.pack_forget()
        self.cancel_button.pack_forget()



    def apply_filters(self, *args):
        """Filtert und sortiert die Aufgaben basierend auf den ausgewählten Kriterien."""
        category_filter = self.filter_category.get()
        priority_filter = self.filter_priority.get()
        sort_by = self.sort_option.get()

        # Mapping für Prioritäten
        priority_mapping = {
            "Sehr Niedrig": 1,
            "Niedrig": 2,
            "Hoch": 3,
            "Sehr Hoch": 4
        }

        # Aufgaben aus der Datenbank laden
        tasks = self.planner.load_entries()

        # Filter anwenden
        if category_filter != "Alle":
            tasks = [task for task in tasks if task.category == category_filter]
        if priority_filter != "Alle":
            priority_value = priority_mapping[priority_filter]
            tasks = [task for task in tasks if task.priority == priority_value]

        # Sortierung anwenden
        if sort_by == "Fälligkeitsdatum":
            tasks.sort(key=lambda task: task.deadline)
        elif sort_by == "Priorität":
            tasks.sort(key=lambda task: task.priority, reverse=True)
        elif sort_by == "Name":
            tasks.sort(key=lambda task: task.name)

        # Treeview aktualisieren
        self.tree.delete(*self.tree.get_children())
        for task in tasks:
            priority_text = self.priority_display_mapping.get(task.priority, "Unbekannt")
            self.tree.insert(
                "", "end",
                values=(task.name, task.deadline.strftime("%Y-%m-%d"), priority_text, task.category)
            )

    def add_attachment(self):
        """Fügt eine Datei oder einen Link zur Aufgabenliste hinzu."""
        new_attachment = tk.simpledialog.askstring("Neuer Anhang", "Gib den Dateipfad oder Link ein:")
        if new_attachment:
            self.attachment_list.insert(tk.END, new_attachment)

    def open_attachment(self):
        """Öffnet den ausgewählten Anhang (Datei oder Link)."""
        selected_index = self.attachment_list.curselection()
        if selected_index:
            attachment = self.attachment_list.get(selected_index)
            if attachment.startswith("http://") or attachment.startswith("https://"):
                import webbrowser
                webbrowser.open(attachment)
            else:
                import os
                if os.path.exists(attachment):
                    os.startfile(attachment)
                else:
                    messagebox.showerror("Fehler", f"Datei '{attachment}' wurde nicht gefunden.")

    def remove_attachment(self):
        """Entfernt den ausgewählten Anhang aus der Liste."""
        selected_index = self.attachment_list.curselection()
        if selected_index:
            self.attachment_list.delete(selected_index)

    
    def add_task(self):
        """Fügt eine neue Aufgabe hinzu und aktualisiert die Anzeige."""
        try:
            # Eingaben aus den Feldern lesen
            name = self.name_entry.get()
            deadline_text = self.deadline_label.cget("text")
            if deadline_text == "Kein Datum ausgewählt":
                raise ValueError("Bitte wählen Sie ein Datum aus.")
            deadline = datetime.strptime(deadline_text, "%Y-%m-%d")

            priority_text = self.selected_priority.get()
            priority_mapping = {
                "Sehr Niedrig": 1,
                "Niedrig": 2,
                "Hoch": 3,
                "Sehr Hoch": 4
            }
            priority = priority_mapping[priority_text]
            category = self.selected_category.get()

            # Anhänge sammeln
            attachments = list(self.attachment_list.get(0, tk.END))

            # Aufgabe erstellen
            self.planner.create_entry(name, deadline, priority, category, text="", links=attachments)

            # Aktualisiere die Treeview
            self.refresh_task_view()

            # Eingabefelder leeren
            self.name_entry.delete(0, tk.END)
            self.deadline_label.config(text="Kein Datum ausgewählt")
            self.attachment_list.delete(0, tk.END)

            messagebox.showinfo("Erfolg", "Aufgabe erfolgreich hinzugefügt!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    
    def update_task(self):
        """Speichert die geänderten Daten der ausgewählten Aufgabe."""
        try:
            # Hole die ausgewählte Zeile in der Treeview
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Fehler", "Bitte eine Aufgabe auswählen!")
                return

            old_name = self.tree.item(selected_item[0], "values")[0]  # Name der Aufgabe vor Änderung

            # Werte aus den Eingabefeldern lesen
            new_name = self.name_entry.get()

            # Deadline aus dem Label auslesen
            deadline_text = self.deadline_label.cget("text")
            if deadline_text == "Kein Datum ausgewählt":
                raise ValueError("Bitte wählen Sie ein Datum aus.")
            new_deadline = datetime.strptime(deadline_text, "%Y-%m-%d")

            priority_text = self.selected_priority.get()
            priority_mapping = {
                "Sehr Niedrig": 1,
                "Niedrig": 2,
                "Hoch": 3,
                "Sehr Hoch": 4
            }
            new_priority = priority_mapping[priority_text]
            new_category = self.selected_category.get()

            # Bearbeitung der Aufgabe
            if old_name == new_name:
                self.planner.edit_entry(new_name, "deadline", new_deadline)
                self.planner.edit_entry(new_name, "priority", new_priority)
                self.planner.edit_entry(new_name, "category", new_category)
            else:
                self.planner.delete_entry(old_name)
                self.planner.create_entry(new_name, new_deadline, new_priority, new_category)

            # Treeview aktualisieren
            self.refresh_task_view()
            messagebox.showinfo("Erfolg", "Aufgabe erfolgreich aktualisiert!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))


            
    def delete_task(self):
        """Löscht die ausgewählte Aufgabe."""
        try:
            # Hole die ausgewählte Zeile in der Treeview
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Fehler", "Bitte eine Aufgabe auswählen!")
                return

            # Hole den Namen der Aufgabe aus der Treeview
            task_name = self.tree.item(selected_item[0], "values")[0]

            # Aufgabe aus dem Planer und der Datenbank löschen
            self.planner.delete_entry(task_name)

            # Aktualisiere die Treeview
            self.refresh_task_view()

            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", f"Die Aufgabe '{task_name}' wurde gelöscht!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))


# Hauptprogramm starten
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyMasterPlanerUI(root)
    root.mainloop()
