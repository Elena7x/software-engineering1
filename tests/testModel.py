import unittest
import os
import sys

# Füge das übergeordnete Verzeichnis zum Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import StudyMasterPlaner

class TestStudyMasterPlaner(unittest.TestCase):
    def setUp(self):
        self.planer = StudyMasterPlaner()
        self.planer.tasks = []

    def test_create_entry(self):
        self.planer.create_entry("Aufgabe 1", "2025-03-20", "", "", "", "")
        self.assertEqual(len(self.planer.tasks), 1)
        self.assertEqual(self.planer.tasks[0].name, "Aufgabe 1")

    def test_no_name(self):
        res = self.planer.create_entry(
        "",                  # name leer
        "","", "", "", ""       # rest darf leer sein
    )
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get("status"), "error")
        self.assertEqual(res.get("message"), "Ungültige Eingabe: Name fehlt")

    def test_delete_entry(self):
        self.planer.create_entry(
            "Aufgabe 1", "2025-04-05", "hoch", "Uni", "Klausur lernen", "2025-04-04"
        )
        self.assertEqual(len(self.planer.tasks), 1)

        # Aufgabe löschen
        result = self.planer.delete_entry("Aufgabe 1")

        # Test: Aufgabe wurde entfernt
        self.assertEqual(len(self.planer.tasks), 0)


if __name__ == '__main__':
    unittest.main()
