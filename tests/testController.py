import unittest
from unittest.mock import MagicMock
import tkinter as tk

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller import AppController

class TestAppController(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.controller = AppController(self.root)

        # Modell durch Mock ersetzen
        self.controller.model = MagicMock()
        self.controller.view = MagicMock()

    def tearDown(self):
        self.root.destroy()

    def test_edit_task_success_default_view(self):
        # Setup: edit_entries gibt True zurück
        self.controller.model.edit_entries.return_value = True

        # Methode aufrufen
        result = self.controller.edit_task(
            old_name="Alt",
            new_name="Neu",
            new_deadline="2025-12-31"
        )

        # Assertions
        self.assertTrue(result)
        self.controller.model.edit_entries.assert_called_once_with(
            "Alt", "Neu", "2025-12-31", None, None, None, None
        )
        self.controller.model.save_to_json.assert_called_once()
        self.controller.view.update_list.assert_called_once_with("list")

if __name__ == "__main__":
    unittest.main()
