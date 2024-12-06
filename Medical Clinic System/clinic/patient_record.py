from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    ''' Class that represents a patient's medical record '''

    def __init__(self, phn=None, autosave=True):
        ''' Construct a patient record '''
        self.phn = phn
        self.autosave = autosave
        self.note_dao = NoteDAOPickle(phn=self.phn, autosave=self.autosave)  # Instantiate NoteDAOPickle

    def search_note(self, code):
        ''' Search for a note in the patient's record '''
        return self.note_dao.search_note(code)

    def create_note(self, text):
        ''' Create a new note in the patient's record '''
        return self.note_dao.create_note(text)

    def retrieve_notes(self, search_string):
        ''' Retrieve notes that match a search string '''
        return self.note_dao.retrieve_notes(search_string)

    def update_note(self, code, new_text):
        ''' Update a note's text '''
        return self.note_dao.update_note(code, new_text)

    def delete_note(self, code):
        ''' Delete a note by its code '''
        return self.note_dao.delete_note(code)

    def list_notes(self):
        ''' List all notes in reverse chronological order '''
        return self.note_dao.list_notes()
