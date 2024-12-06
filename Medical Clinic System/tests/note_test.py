from unittest import TestCase
import unittest  # Add this import if not already present
from clinic.note import Note
import datetime

class NoteTest(TestCase):
    def setUp(self):
        # Generate a fixed timestamp once
        self.timestamp = datetime.datetime.now()
        self.note = Note(1, "Patient shows up with chest pain", self.timestamp)

    def test_eq(self):
        # Use the same timestamp for all notes
        same_note = Note(1, "Patient shows up with chest pain", self.timestamp)
        different_note_1 = Note(2, "Patient shows up with chest pain", self.timestamp)
        different_note_2 = Note(1, "Patient has dizziness", self.timestamp)
        self.assertTrue(self.note == self.note)
        self.assertTrue(self.note == same_note)
        self.assertFalse(self.note == different_note_1)
        self.assertFalse(self.note == different_note_2)

    def test_str(self):
        # Use the same timestamp for all notes
        same_note = Note(1, "Patient shows up with chest pain", self.timestamp)
        different_note_1 = Note(2, "Patient shows up with chest pain", self.timestamp)
        different_note_2 = Note(1, "Patient has dizziness", self.timestamp)
        expected_str = f"1; {self.timestamp}; Patient shows up with chest pain"
        self.assertEqual(expected_str, str(self.note))
        self.assertEqual(expected_str, str(same_note))
        self.assertEqual(f"2; {self.timestamp}; Patient shows up with chest pain", str(different_note_1))
        self.assertEqual(f"1; {self.timestamp}; Patient has dizziness", str(different_note_2))
        self.assertEqual(str(same_note), str(self.note))
        self.assertNotEqual(str(different_note_1), str(self.note))
        self.assertNotEqual(str(different_note_2), str(self.note))

    def test_repr(self):
        # Use the same timestamp for all notes
        same_note = Note(1, "Patient shows up with chest pain", self.timestamp)
        different_note_1 = Note(2, "Patient shows up with chest pain", self.timestamp)
        different_note_2 = Note(1, "Patient has dizziness", self.timestamp)
        expected_repr = f"Note(1, {repr(self.timestamp)}, 'Patient shows up with chest pain')"
        self.assertEqual(expected_repr, repr(self.note))
        self.assertEqual(expected_repr, repr(same_note))
        self.assertEqual(f"Note(2, {repr(self.timestamp)}, 'Patient shows up with chest pain')", repr(different_note_1))
        self.assertEqual(f"Note(1, {repr(self.timestamp)}, 'Patient has dizziness')", repr(different_note_2))
        self.assertEqual(repr(same_note), repr(self.note))
        self.assertNotEqual(repr(different_note_1), repr(self.note))
        self.assertNotEqual(repr(different_note_2), repr(self.note))

if __name__ == '__main__':
    unittest.main()
