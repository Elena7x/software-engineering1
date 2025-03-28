import unittest
import os
import sys

# Füge das übergeordnete Verzeichnis zum Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import StudyMasterPlaner

class TestStudyMasterPlaner(unittest.TestCase):
    def setUp(self):
        self.planer = StudyMasterPlaner()

    def test_create_entry(self):
        self.planer.create_entry("Aufgabe 1", "2025-03-20")
        self.assertEqual(len(self.planer.tasks), 1)
        self.assertEqual(self.planer.tasks[0].name, "Aufgabe 1")

if __name__ == '__main__':
    unittest.main()
