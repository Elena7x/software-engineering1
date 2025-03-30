from model import StudyMasterPlaner
from view import StudyMasterPlannerView  # Wichtig: nicht CalendarView direkt importieren!

class AppController:
    def __init__(self, root):
        self.model = StudyMasterPlaner()
        self.view = StudyMasterPlannerView(root, self)

    def load_task(self):
        pass 

    def add_task(self, name, deadline):
        self.model.create_entry(name, deadline)
        self.view.update_list()

    def remove_task(self, name):
        self.model.delete_entry(name)
        self.view.update_list()

    def edit_task(self, name):
        pass 
