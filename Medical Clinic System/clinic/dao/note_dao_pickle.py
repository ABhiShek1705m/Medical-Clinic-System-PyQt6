import os
import pickle
import time
from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
import datetime


class NoteDAOPickle(NoteDAO):
    ''' DAO class for managing notes using pickle serialization '''

    def __init__(self, phn=None, autosave=True):
        ''' Initialize the NoteDAOPickle '''
        self.phn = phn
        self.autosave = autosave
        self.file_path = f'clinic/records/{self.phn}.dat'

        # Initialize the notes dictionary and code counter
        self.notes = {}
        self.code_counter = 0

        # Load notes if autosave is enabled
        if self.autosave:
            self.load_notes()

    def load_notes(self):
        ''' Load notes from the patient's record file '''
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as file:
                # Load the notes dictionary
                self.notes = pickle.load(file)
                # Update the code counter to the highest existing code
                if self.notes:
                    self.code_counter = max(self.notes.keys())
                else:
                    self.code_counter = 0
        else:
            # If file doesn't exist, start with empty notes and counter at 0
            self.notes = {}
            self.code_counter = 0

    def save_notes(self):
        ''' Save the current notes to the patient's record file '''
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'wb') as file:
            # Serialize the notes dictionary into the binary file
            pickle.dump(self.notes, file)

    def search_note(self, code):
        ''' Search for a note by code '''
        return self.notes.get(code)

    def create_note(self, text):
        ''' Add a new note '''
        # Increment the code counter
        self.code_counter += 1
        code = self.code_counter
        timestamp = datetime.datetime.now()
        note = Note(code=code, text=text, timestamp=timestamp)
        self.notes[code] = note

        # Save notes if autosave is enabled
        if self.autosave:
            self.save_notes()

        return note

    def retrieve_notes(self, search_string):
        ''' Retrieve notes that contain the search string '''
        retrieved_notes = []
        for note in self.notes.values():
            if search_string in note.text:
                retrieved_notes.append(note)
        return retrieved_notes

    def update_note(self, code, new_text):
        ''' Update an existing note '''
        note = self.notes.get(code)
        if not note:
            return False

        note.text = new_text

        # Save notes if autosave is enabled
        if self.autosave:
            self.save_notes()

        return True

    def delete_note(self, code):
        ''' Remove a note by code '''
        if code in self.notes:
            del self.notes[code]

            # Save notes if autosave is enabled
            if self.autosave:
                self.save_notes()

            return True
        else:
            return False

    def list_notes(self):
        ''' List all notes in reverse order '''
        # Return notes sorted by code in descending order
        return sorted(self.notes.values(), key=lambda note: note.code, reverse=True)