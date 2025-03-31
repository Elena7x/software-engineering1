from model import StudyMasterPlaner
from view import StudyMasterPlannerView

class AppController:
    def __init__(self, root):
        self.model = StudyMasterPlaner()
        self.view = StudyMasterPlannerView(root, self)

    def load_task(self, name):
        task = self.model.load_entry(name)
        if task:
            return {
                "name": task.name,
                "deadline": task.deadline,
                "priority": task.priority,
                "category": task.category
            }
        return None

    def add_task(self, name, deadline, view="list"):
        self.model.create_entry(name, deadline)
        self.view.update_list(view)

    def remove_task(self, name, view="list"):
        self.model.delete_entry(name)
        self.model.save_to_json() 
        self.view.update_list(view)


    def edit_task(self, old_name, new_name=None, new_deadline=None, view="list"):
        success = self.model.edit_entries(old_name, new_name, new_deadline)
        if success:
            self.model.save_to_json()
            self.view.update_list(view)
        return success


