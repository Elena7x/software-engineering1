import tkinter as tk
import calendar
from datetime import datetime
from tkinter import ttk

class StudyMasterPlannerView:
    # Hier wird Ansicht für mögliche Aktionen angezeigt
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Study Master Planner")
        self.root.geometry("500x400")

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
        btn_calendar = tk.Button(button_frame, text="Kalender anzeigen", command=self.show_calendar)
        btn_calendar.place(relx=0.5, rely=0.2, relwidth=0.5, anchor="center")  # 30% der Breite, zentriert

        btn_list = tk.Button(button_frame, text="Liste anzeigen",command=lambda: print("Liste-Button geklickt!"))
        btn_list.place(relx=0.5, rely=0.3, relwidth=0.5, anchor="center")

    def show_task_input(self):
        """ Öffnet die Eingabemaske für eine neue Aufgabe """
        self.root.withdraw()  # Hauptfenster verstecken
        Task(self.root)  # Erstellt das Fenster

    def show_calendar(self):
        self.root.withdraw()  # Hauptfenster verstecken
        CalendarView(self.root, self.controller)


class Task:
    def __init__(self, parent):
        """ Erstellt eine Eingabemaske für neue Aufgaben """
        self.top = tk.Toplevel(parent)  # Neues Fenster Eingabemaske
        self.top.title("Neue Aufgabe hinzufügen")
        self.parent = parent #Hauptfenster
        self.top.geometry("500x400")
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

        # Event für das rote X (WM_DELETE_WINDOW) registrieren
        self.top.protocol("WM_DELETE_WINDOW", self.go_back)

        btn_go_back = tk.Button(button_frame, text="Go Back", command=self.go_back)
        btn_go_back.pack(side=tk.RIGHT, padx=10)

    def go_back(self):
        """ Zeigt das Hauptfenster wieder an und schließt die Eingabemaske """
        self.parent.deiconify()  # Hauptfenster wieder sichtbar machen
        self.top.destroy()  # Eingabemaske schließen

class CalendarView:
    def __init__(self, parent, controller=None):
        self.controller = controller
        self.top = tk.Toplevel(parent)
        self.top.title("Kalender")
        self.parent = parent
        self.top.geometry("600x500")

        self.today = datetime.today()
        self.year = self.today.year
        self.month = self.today.month

        # Monatsanzeige
        self.label_month = tk.Label(self.top, font=("Arial", 16))
        self.label_month.pack(pady=5)

        # Kalender-Frame (wird bei Redraw gelöscht)
        self.calendar_frame = tk.Frame(self.top)
        self.calendar_frame.pack()

        # Button-Frame bleibt bestehen
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Vorheriger Monat", command=self.prev_month).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Nächster Monat", command=self.next_month).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Zurück", command=self.go_back).pack(side=tk.RIGHT, padx=5)

        self.top.protocol("WM_DELETE_WINDOW", self.go_back)

        self.draw_calendar()

    def draw_calendar(self):
        # Monatslabel aktualisieren
        month_name = calendar.month_name[self.month]
        self.label_month.config(text=f"{month_name} {self.year}")

        # alten Kalender löschen
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(self.year, self.month)

        # Wochentage
        days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, width=10, borderwidth=1, relief="solid").grid(row=0, column=col)

        # Tage
        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="", width=10, height=4, relief="solid").grid(row=row, column=col)
                else:
                    text = str(day)
                    date_str = f"{self.year}-{self.month:02}-{day:02}"
                    tasks = self.get_tasks_for_date(date_str)
                    if tasks:
                        max_len = 12  # Max. Zeichen pro Titel
                        for t in tasks:
                            name = t.name if len(t.name) <= max_len else t.name[:max_len] + "..."
                            text += "\n" + name
                    if tasks:
                        btn = tk.Button(
                            self.calendar_frame,
                            text=text,
                            width=10,
                            height=4,
                            relief="raised",
                            anchor="n",
                            justify="left",
                            wraplength=80,
                            command=lambda d=date_str, t=tasks: self.open_day_task_list(d, t)
                        )
                        btn.grid(row=row, column=col)
                    else:
                        tk.Label(self.calendar_frame, text=text, width=10, height=4, relief="solid").grid(row=row, column=col)

    def get_tasks_for_date(self, date_str):
        if self.controller:
            return [task for task in self.controller.model.tasks if task.deadline == date_str]
        return []
    
    def open_day_task_list(self, date_str, tasks):
        DayTaskList(self.top, date_str, tasks, self.controller, self)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.draw_calendar()

    def go_back(self):
        self.parent.deiconify()
        self.top.destroy()
        
class DayTaskList:
    def __init__(self, parent, date_str, tasks, controller, calendar_view):
        self.controller = controller
        self.calendar_view = calendar_view  # <--- Das ist neu!

        self.top = tk.Toplevel(parent)
        self.top.title(f"Aufgaben am {date_str}")
        self.top.geometry("400x300")

        tk.Label(self.top, text=f"Aufgaben für {date_str}:", font=("Arial", 12, "bold")).pack(pady=10)

        for task in tasks:
            frame = tk.Frame(self.top)
            frame.pack(fill=tk.X, padx=10, pady=5)

            lbl = tk.Label(frame, text=task.name, anchor="w")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            btn = tk.Button(frame, text="Bearbeiten", command=lambda t=task: self.open_edit_window(t))
            btn.pack(side=tk.RIGHT)

        tk.Button(self.top, text="Schließen", command=self.top.destroy).pack(pady=10)
    
    
    def open_edit_window(self, task):
        win = tk.Toplevel(self.top)
        win.title("Aufgabe bearbeiten")
        win.geometry("400x250")

        tk.Label(win, text="Titel:").pack(pady=5)
        entry_title = tk.Entry(win, width=40)
        entry_title.insert(0, task.name)
        entry_title.pack(pady=5)

        tk.Label(win, text="Deadline (YYYY-MM-DD):").pack(pady=5)
        entry_deadline = tk.Entry(win, width=40)
        entry_deadline.insert(0, task.deadline)
        entry_deadline.pack(pady=5)

        def save_changes():
            new_name = entry_title.get()
            new_deadline = entry_deadline.get()
            self.controller.model.edit_entries(task.name, new_name, new_deadline)
            self.controller.model.save_to_json()

            win.destroy()
            self.top.destroy()
            self.calendar_view.top.destroy()  # <--- altes Kalenderfenster schließen

            # neues Kalenderfenster öffnen
            CalendarView(self.controller.view.root, self.controller)

        tk.Button(win, text="Speichern", command=save_changes).pack(pady=10)


''' def create_task_input_section(self, parent_frame):
        self.task_input_frame = tk.Frame(parent_frame, bd=2, relief=tk.SUNKEN, padx=10, pady=10)
        self.task_input_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(self.task_input_frame, text="Aufgabenbeschreibung:").grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(self.task_input_frame, width=50)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.task_input_frame, text="Hinzufügen", command=self.add_task).grid(row=0, column=2, padx=5)
        tk.Button(self.task_input_frame, text="Abbrechen", command=self.hide_task_input).grid(row=0, column=3, padx=5)

        self.task_input_frame.pack_forget()  # Versteckt das Eingabefeld anfangs

    def create_task_view(self, parent_frame):
        self.tree = ttk.Treeview(parent_frame, columns=("Task",), show="headings")
        self.tree.heading("Task", text="Aufgabe")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        button_frame = tk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(button_frame, text="Aufgabe löschen", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Auswahl aufheben", command=self.cancel_selection).pack(side=tk.LEFT, padx=5)

    def refresh_task_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Hier würden echte Daten aus einem Controller nachgeladen werden

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            task = self.tree.item(selected_item, "values")[0]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task)
            self.show_task_input()

    def show_task_input(self):
        self.task_input_frame.pack(fill=tk.X)

    def hide_task_input(self):
        self.task_input_frame.pack_forget()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            self.tree.insert("", "end", values=(task_text,))
            self.task_entry.delete(0, tk.END)
            self.hide_task_input()

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def cancel_selection(self):
        self.tree.selection_remove(self.tree.selection())'''


'''

class ListView:
    def __init__(self, ui, controller):

    def draw_list(self):

    def update_list(self):

    def show_only_selected(self):'''

if __name__ == "__main__":
    root = tk.Tk()  # Erstelle das Hauptfenster
    app = StudyMasterPlannerView(root)  # Initialisiere die Klasse
    root.mainloop()  # Starte das Tkinter-Event-Loop

