import tkinter as tk
import calendar
from datetime import datetime
from tkinter import messagebox

class StudyMasterPlannerView:
    # Hier wird Ansicht für mögliche Aktionen angezeigt
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Study Master Planner")
        self.root.geometry("800x600")

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

        btn_list = tk.Button(button_frame, text="Liste anzeigen", command=self.show_list_view)
        btn_list.place(relx=0.5, rely=0.3, relwidth=0.5, anchor="center")

    def show_task_input(self):
        """ Öffnet die Eingabemaske für eine neue Aufgabe """
        self.root.withdraw()  # Hauptfenster verstecken
        TaskView(self.root, self.controller)  # Erstellt das Fenster

    def show_calendar(self):
        self.root.withdraw()  # Hauptfenster verstecken
        CalendarView(self.root, self.controller)
        
    def show_list_view(self):
        ListView(self.root, self.controller)
        
    def update_list(self, view):
        if view == "calendar":
            # Kalender schließen, wenn offen
            for window in self.root.winfo_children():
                if isinstance(window, tk.Toplevel) and window.title() == "Kalender":
                    window.destroy()
            CalendarView(self.root, self.controller)

        elif view == "list":
            # ListView schließen, wenn offen
            for window in self.root.winfo_children():
                if isinstance(window, tk.Toplevel) and window.title() == "Alle Aufgaben":
                    window.destroy()
            ListView(self.root, self.controller)

    def show_alert(self, status, message):
        if status == "error":
            messagebox.showerror("Error", message)
        if status == "info":
            messagebox.showinfo("Info", message)


class TaskView:
    def __init__(self, parent, controller):
        self.controller = controller
        """ Erstellt eine Eingabemaske für neue Aufgaben """
        self.top = tk.Toplevel(parent)  # Neues Fenster Eingabemaske
        self.top.title("Neue Aufgabe hinzufügen")
        self.parent = parent #Hauptfenster
        self.top.geometry("600x600")
        # Label und Eingabefeld
        tk.Label(self.top, text="Name").pack(pady=5)    #Eingabe Aufgabenname
        self.name_entry = tk.Entry(self.top, width=40)
        self.name_entry.pack(pady=5)

        tk.Label(self.top, text="Deadline").pack(pady=5)    #Eingabe Deadline
        self.deadline_entry = tk.Entry(self.top, width=40)
        self.deadline_entry.pack(pady=5)

        tk.Label(self.top, text="Priorität").pack(pady=5)    #Eingabe Priorität
        self.priority_entry = tk.Entry(self.top, width=40)
        self.priority_entry.pack(pady=5)

        tk.Label(self.top, text="Kategorie").pack(pady=5)  # Eingabe Kategorie
        self.category_entry = tk.Entry(self.top, width=40)
        self.category_entry.pack(pady=5)

        tk.Label(self.top, text="Beschreibung").pack(pady=5)  # Eingabe Beschreibung
        self.description_entry = tk.Entry(self.top, width=40)
        self.description_entry.pack(pady=5)

        tk.Label(self.top, text="Erinnerung").pack(pady=5)  # Eingabe Erinnerung
        self.reminder_entry = tk.Entry(self.top, width=40)
        self.reminder_entry.pack(pady=5)

        # Buttons für Speichern und Abbrechen
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=10)

        btn_save = tk.Button(button_frame, text="Speichern", command=self.save_task)
        btn_save.pack(side=tk.LEFT, padx=10)

        # Event für das rote X (WM_DELETE_WINDOW) registrieren
        self.top.protocol("WM_DELETE_WINDOW", self.go_back)

        btn_go_back = tk.Button(button_frame, text="Zurück", command=self.go_back)
        btn_go_back.pack(side=tk.RIGHT, padx=10)

    def go_back(self):
        """ Zeigt das Hauptfenster wieder an und schließt die Eingabemaske """
        self.parent.deiconify()  # Hauptfenster wieder sichtbar machen
        self.top.destroy()  # Eingabemaske schließen

    def save_task(self):
        task_data = {
            "name": self.name_entry.get(),
            "deadline": self.deadline_entry.get(),
            "priority": self.priority_entry.get(),
            "category": self.category_entry.get(),
            "description": self.description_entry.get(),
            "reminder": self.reminder_entry.get()
        }
        self.controller.add_task(task_data)  # direkt Controller informieren
        self.go_back()

class CalendarView:
    def __init__(self, parent, controller=None):
        self.controller = controller
        self.top = tk.Toplevel(parent)
        self.top.title("Kalender")
        self.parent = parent
        self.top.geometry("600x600")

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
        self.top.geometry("600x600")

        tk.Label(self.top, text=f"Aufgaben für {date_str}:", font=("Arial", 12, "bold")).pack(pady=10)

        for task in tasks:
            frame = tk.Frame(self.top)
            frame.pack(fill=tk.X, padx=10, pady=5)

            lbl = tk.Label(frame, text=task.name, anchor="w")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Mülleimer-Button 
            btn_delete = tk.Button(frame, text="🗑", width=2, command=lambda t=task: self.delete_task(t))
            btn_delete.pack(side=tk.RIGHT)

            # Bearbeiten-Button
            btn_edit = tk.Button(frame, text="Bearbeiten", command=lambda t=task: self.open_edit_window(t))
            btn_edit.pack(side=tk.RIGHT, padx=(5, 2))

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
            self.controller.edit_task(task.name, new_name, new_deadline,  view="calendar")

            win.destroy()
            self.top.destroy()
            self.calendar_view.top.destroy()

        tk.Button(win, text="Speichern", command=save_changes).pack(pady=10)

    def delete_task(self, task):
        self.controller.remove_task(task.name, view="calendar")
        self.top.destroy()
        self.calendar_view.top.destroy()

class ListView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.top = tk.Toplevel(parent)
        self.top.title("Alle Aufgaben")
        self.top.geometry("500x400")

        tk.Label(self.top, text="Aufgabenübersicht", font=("Arial", 14, "bold")).pack(pady=10)

        self.list_frame = tk.Frame(self.top)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.draw_list()

        btn_close = tk.Button(self.top, text="Schließen", command=self.top.destroy)
        btn_close.pack(pady=10)

    def draw_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for task in self.controller.model.tasks:
            frame = tk.Frame(self.list_frame, bd=1, relief=tk.RIDGE)
            frame.pack(fill=tk.X, padx=10, pady=5)

            lbl_text = (
                f"📌 {task.name}  |  "
                f"📅 {task.deadline}  |  "
                f"⭐ Priorität: {task.priority}  |  "
                f"📁 Kategorie: {task.category}"
            )

            tk.Label(frame, text=lbl_text, anchor="w").pack(side=tk.LEFT, padx=5, pady=5)

            # 🗑 Mülleimer-Button
            btn_delete = tk.Button(frame, text="🗑", width=2, command=lambda t=task: self.delete_task(t))
            btn_delete.pack(side=tk.RIGHT)

            # 🖊 Bearbeiten-Button
            btn_edit = tk.Button(frame, text="Bearbeiten", command=lambda t=task: self.open_edit_window(t))
            btn_edit.pack(side=tk.RIGHT, padx=(5, 2))

    def open_edit_window(self, task):
        win = tk.Toplevel(self.top)
        win.title("Aufgabe bearbeiten")
        win.geometry("400x400")

        tk.Label(win, text="Titel:").pack(pady=5)
        entry_title = tk.Entry(win, width=40)
        entry_title.insert(0, task.name)
        entry_title.pack(pady=5)

        tk.Label(win, text="Deadline (YYYY-MM-DD):").pack(pady=5)
        entry_deadline = tk.Entry(win, width=40)
        entry_deadline.insert(0, task.deadline)
        entry_deadline.pack(pady=5)

        tk.Label(win, text="Priorität:").pack(pady=5)
        entry_priority = tk.Entry(win, width=40)
        entry_priority.insert(0, task.name)
        entry_priority.pack(pady=5)

        tk.Label(win, text="Kategorie:").pack(pady=5)
        entry_category = tk.Entry(win, width=40)
        entry_category.insert(0, task.name)
        entry_category.pack(pady=5)

        tk.Label(win, text="Beschreibung:").pack(pady=5)
        entry_description = tk.Entry(win, width=40)
        entry_description.insert(0, task.name)
        entry_description.pack(pady=5)

        tk.Label(win, text="Erinnerung:").pack(pady=5)
        entry_reminder = tk.Entry(win, width=40)
        entry_reminder.insert(0, task.name)
        entry_reminder.pack(pady=5)

        def save_changes():
            new_name = entry_title.get()
            new_deadline = entry_deadline.get()
            new_priority = entry_priority.get()
            new_category = entry_category.get()
            new_description = entry_description.get()
            new_reminder = entry_reminder.get()
            self.controller.edit_task(task.name, new_name, new_deadline, new_priority, new_category, new_description, new_reminder, view="list")
            win.destroy()

        tk.Button(win, text="Speichern", command=save_changes).pack(pady=10)
    
    def delete_task(self, task):
        self.controller.remove_task(task.name, view="list")


if __name__ == "__main__":
    root = tk.Tk()  # Erstelle das Hauptfenster
    app = StudyMasterPlannerView(root)  # Initialisiere die Klasse
    root.mainloop()  # Starte das Tkinter-Event-Loop

