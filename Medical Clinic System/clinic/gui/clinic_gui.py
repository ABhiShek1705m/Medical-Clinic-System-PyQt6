import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLineEdit, QLabel,
    QPushButton, QVBoxLayout, QMessageBox, QDialog, QDialogButtonBox, 
    QFormLayout, QInputDialog, QTableView, QPlainTextEdit
)

# Import necessary modules and exceptions from the clinic package
from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class ClinicGUI(QMainWindow):
    """
    This class represents the main GUI window for the Medical Clinic System.
    It handles user interactions and displays different screens based on the user's actions.
    """

    def __init__(self):
        super().__init__()

         # Initialize the controller with autosave enabled
        self.controller = Controller(autosave=True)

        # Set the window title and size
        self.setWindowTitle("Medical Clinic System")
        self.resize(600, 400)

        self.initUI()

    def initUI(self):

        # Create a central widget that will hold all other widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Display the login screen
        self.login_screen()

    def login_screen(self):
        """
        Displays the login screen where users can enter their username and password.
        """
        # Create a vertical layout to arrange widgets vertically
        layout = QVBoxLayout()

        # Create labels and line edits for username and password
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        # Set the password input to hide the characters
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Create a login button and connect it to the login method
        self.login_button = QPushButton("Log in")
        self.login_button.clicked.connect(self.login)

        # Add widgets to the layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        

        # Set the layout for the central widget
        self.central_widget.setLayout(layout)

    def login(self):
        """
        Handles the login process when the user clicks the login button.
        """
        # Get the username and password from the input fields
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            # Attempt to log in using the controller
            self.controller.login(username, password)
            # Show a success message
            QMessageBox.information(self, "Login Successful", "Logged in successfully.")
            # Proceed to the main menu
            self.main_menu()
        except InvalidLoginException:
            # Show an error message if login fails
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def main_menu(self):
        """
        Displays the main menu after the user has successfully logged in.
        """
        # Clear the central widget
        self.central_widget.deleteLater()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the main menu buttons
        layout = QVBoxLayout()

        # Create buttons for each main menu option
        self.create_patient_button = QPushButton("Add new patient")
        self.create_patient_button.clicked.connect(self.create_patient)

        self.search_patient_button = QPushButton("Search patient by PHN")
        self.search_patient_button.clicked.connect(self.search_patient)

        self.retrieve_patients_button = QPushButton("Retrieve patients by name")
        self.retrieve_patients_button.clicked.connect(self.retrieve_patients_by_name)

        self.update_patient_button = QPushButton("Change patient data")
        self.update_patient_button.clicked.connect(self.update_patient)

        self.delete_patient_button = QPushButton("Remove patient")
        self.delete_patient_button.clicked.connect(self.delete_patient) 

        self.list_patients_button = QPushButton("List all patients")
        self.list_patients_button.clicked.connect(self.list_all_patients) 

        self.start_appointment_button = QPushButton("Start appointment with patient")
        self.start_appointment_button.clicked.connect(self.start_appointment)

        self.logout_button = QPushButton("Log out")
        self.logout_button.clicked.connect(self.logout)

        # Add all buttons to the layouts
        layout.addWidget(self.create_patient_button)
        layout.addWidget(self.search_patient_button)
        layout.addWidget(self.retrieve_patients_button)
        layout.addWidget(self.update_patient_button)
        layout.addWidget(self.delete_patient_button)
        layout.addWidget(self.list_patients_button)
        layout.addWidget(self.start_appointment_button)
        layout.addWidget(self.logout_button)

        # Set the layout for the central widget
        self.central_widget.setLayout(layout)

    def create_patient(self):
        """
        Opens a dialog to create a new patient and add them to the system.
        """
        # Create a dialog window for adding a new patient
        dialog = QDialog(self)
        dialog.setWindowTitle("Add new patient")

        # Use a form layout to arrange labels and input fields
        form_layout = QFormLayout()
        phn_input = QLineEdit()
        name_input = QLineEdit()
        birth_date_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()
        address_input = QLineEdit()

        # Add input fields to the form layout with labels
        form_layout.addRow("Personal Health Number (PHN):", phn_input)
        form_layout.addRow("Full name:", name_input)
        form_layout.addRow("Birth date (YYYY-MM-DD):", birth_date_input)
        form_layout.addRow("Phone number:", phone_input)
        form_layout.addRow("Email:", email_input)
        form_layout.addRow("Address:", address_input)

        # Add OK and Cancel buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        form_layout.addWidget(button_box)

        dialog.setLayout(form_layout)
        # Execute the dialog and check if the user pressed OK
        if dialog.exec():
            try:
                # Get the input data from the user
                phn = int(phn_input.text())
                name = name_input.text()
                birth_date = birth_date_input.text()
                phone = phone_input.text()
                email = email_input.text()
                address = address_input.text()
                # Use the controller to create a new patient
                self.controller.create_patient(phn, name, birth_date, phone, email, address)
                # Show a success message
                QMessageBox.information(self, "Success", "Patient added to the system.")
            except IllegalAccessException:
                # Show an error if the user is not logged in
                QMessageBox.warning(self, "Error", "Must login first.")
            except IllegalOperationException:
                # Show an error if the PHN already exists
                QMessageBox.warning(
                    self, "Error", f"There is a patient already registered with PHN {phn}."
                )
            except ValueError:
                # Show an error if PHN is not an integer
                QMessageBox.warning(self, "Error", "PHN must be an integer.")

    def search_patient(self):
        """
        Allows the user to search for a patient by their Personal Health Number (PHN).
        """
        # Prompt the user to enter the PHN
        phn, ok = QInputDialog.getInt(self, "Search patient", "Personal Health Number (PHN):")
        if ok:
            try:
                # Search for the patient using the controller
                patient = self.controller.search_patient(phn)
                if patient:
                    # If found, display the patient's data
                    self.show_patient_data(patient)
                else:
                    # If not found, inform the user
                    QMessageBox.information(self, "No patient found", "There is no patient registered with this PHN.")
            except IllegalAccessException:
                # Show an error if the user is not logged in
                QMessageBox.warning(self, "Error", "Must login first.")
    
    
    def show_patient_data(self, patient):
        """
        Displays the patient's data in a message box.
        """
        # Format the patient's data into a string
        message = (
            f"PHN: {patient.phn}\n"
            f"Name: {patient.name}\n"
            f"Birth date: {patient.birth_date}\n"
            f"Phone: {patient.phone}\n"
            f"Email: {patient.email}\n"
            f"Address: {patient.address}"
        )
        # Show the data in an information message box
        QMessageBox.information(self, "Patient Data", message)

    def retrieve_patients_by_name(self):
        """
        Retrieves patients whose names match a search string provided by the user.
        """
        # Prompt the user to enter a name to search for
        search_string, ok = QInputDialog.getText(self, "Retrieve patients by name", "Search for:")
        if ok:
            try:
                # Retrieve patients matching the search string
                found_patients = self.controller.retrieve_patients(search_string)
                if found_patients:
                    # If patients are found, display them in a table
                    self.show_patients_table(found_patients)
                else:
                    # If no patients are found, inform the user
                    QMessageBox.information(
                        self, "No patients found", f"No patients found with name: {search_string}"
                    )
            except IllegalAccessException:
                # Show an error if the user is not logged in
                QMessageBox.warning(self, "Error", "Must login first.")

    
    def show_patients_table(self, patients):
        """
        Displays a list of patients in a QTableView within a dialog.
        """
        # Create a QTableView widget
        table_view = QTableView(self)

        # Create a model for the table
        model = QStandardItemModel(len(patients), 6)  # Rows and Columns
        model.setHorizontalHeaderLabels(["PHN", "Name", "Birth date", "Phone", "Email", "Address"])

        # Populate the model with patient data
        for row, patient in enumerate(patients):
            model.setItem(row, 0, QStandardItem(str(patient.phn)))
            model.setItem(row, 1, QStandardItem(patient.name))
            model.setItem(row, 2, QStandardItem(patient.birth_date))
            model.setItem(row, 3, QStandardItem(patient.phone))
            model.setItem(row, 4, QStandardItem(patient.email))
            model.setItem(row, 5, QStandardItem(patient.address))

        # Set the model for the table view
        table_view.setModel(model)
        table_view.resizeColumnsToContents()  # Resize columns to fit content

        # Create a dialog to display the table view
        dialog = QDialog(self)
        dialog.setWindowTitle("Patients")
        layout = QVBoxLayout()
        layout.addWidget(table_view)
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec()

    
    def update_patient(self):
        """
        Allows the user to update an existing patient's data.
        """
        # Prompt the user to enter the PHN of the patient to update
        phn, ok = QInputDialog.getInt(self, "Change patient data", "Personal Health Number (PHN):")
        if ok:
            try:
                # Search for the patient using the controller
                patient = self.controller.search_patient(phn)
                if patient:
                    # Create a dialog to input new data
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Update Patient Data")

                    # Form layout for input fields with placeholders showing current data
                    form_layout = QFormLayout()
                    phn_input = QLineEdit()
                    phn_input.setPlaceholderText(str(patient.phn))
                    name_input = QLineEdit()
                    name_input.setPlaceholderText(patient.name)
                    birth_date_input = QLineEdit()
                    birth_date_input.setPlaceholderText(patient.birth_date)
                    phone_input = QLineEdit()
                    phone_input.setPlaceholderText(patient.phone)
                    email_input = QLineEdit()
                    email_input.setPlaceholderText(patient.email)
                    address_input = QLineEdit()
                    address_input.setPlaceholderText(patient.address)

                    # Add input fields to the form layout
                    form_layout.addRow("Personal Health Number (PHN):", phn_input)
                    form_layout.addRow("Full name:", name_input)
                    form_layout.addRow("Birth date (YYYY-MM-DD):", birth_date_input)
                    form_layout.addRow("Phone number:", phone_input)
                    form_layout.addRow("Email:", email_input)
                    form_layout.addRow("Address:", address_input)

                    # Add OK and Cancel buttons
                    button_box = QDialogButtonBox(
                        QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
                    )
                    button_box.accepted.connect(dialog.accept)
                    button_box.rejected.connect(dialog.reject)
                    form_layout.addWidget(button_box)

                    dialog.setLayout(form_layout)
                    # Execute the dialog and check if the user pressed OK
                    if dialog.exec():
                        # Get the new data from the inputs
                        new_phn_text = phn_input.text()
                        new_name = name_input.text()
                        new_birth_date = birth_date_input.text()
                        new_phone = phone_input.text()
                        new_email = email_input.text()
                        new_address = address_input.text()

                        # Use existing data if new inputs are empty
                        new_phn = int(new_phn_text) if new_phn_text else patient.phn
                        new_name = new_name if new_name else patient.name
                        new_birth_date = (
                            new_birth_date if new_birth_date else patient.birth_date
                        )
                        new_phone = new_phone if new_phone else patient.phone
                        new_email = new_email if new_email else patient.email
                        new_address = new_address if new_address else patient.address

                        # Confirm the update with the user
                        confirm = QMessageBox.question(
                            self,
                            "Confirm Update",
                            f"Are you sure you want to change patient data {patient.name}?",
                        )
                        if confirm == QMessageBox.StandardButton.Yes:
                            # Update the patient data using the controller
                            self.controller.update_patient(
                                phn,
                                new_phn,
                                new_name,
                                new_birth_date,
                                new_phone,
                                new_email,
                                new_address,
                            )
                            # Inform the user of success
                            QMessageBox.information(self, "Success", "Patient data changed.")
                    # If the patient is not found, show an error
                    else:
                        QMessageBox.warning(
                            self, "Error", "There is no patient registered with this PHN."
                        )
            except IllegalAccessException:
                # Show an error if the user is not logged in
                QMessageBox.warning(self, "Error", "Must login first.")
            except IllegalOperationException:
                QMessageBox.warning(self, "Error", str(IllegalOperationException))


    def delete_patient(self):
        """
        Allows the user to delete a patient from the system.
        """
        # Prompt the user to enter the PHN of the patient to delete
        phn, ok = QInputDialog.getInt(self, "Remove patient", "Personal Health Number (PHN):")
        if ok:
            try:
                # Search for the patient using the controller
                patient = self.controller.search_patient(phn)
                if patient:
                    # Confirm the deletion with the user
                    confirm = QMessageBox.question(
                        self,
                        "Confirm Delete",
                        f"Are you sure you want to remove patient {patient.name}?",
                    )
                    if confirm == QMessageBox.StandardButton.Yes:
                        # Delete the patient using the controller
                        self.controller.delete_patient(phn)
                        # Inform the user of success
                        QMessageBox.information(
                            self, "Success", "Patient removed from the system."
                        )
                else:
                    # Show an error if the patient is not found
                    QMessageBox.warning(
                        self, "Error", "There is no patient registered with this PHN."
                    )
            except IllegalAccessException:
                # Show an error if the user is not logged in
                QMessageBox.warning(self, "Error", "Must login first.")
            except IllegalOperationException:
                QMessageBox.warning(self, "Error", str(IllegalOperationException))


    def list_all_patients(self):
        """
        Lists all patients currently registered in the system.
        """
        try:
            # Get the list of all patients from the controller
            patients = self.controller.list_patients()
            if patients:
                # Display the patients in a table
                self.show_patients_table(patients)
            else:
                # Inform the user if there are no patients
                QMessageBox.information(self, "No patients", "No patients registered in the clinic.")
        except IllegalAccessException:
            # Show an error if the user is not logged in
            QMessageBox.warning(self, "Error", "Must login first.")


    def start_appointment(self):
        """
        Starts an appointment with a patient by setting the current patient.
        """
        # Prompt the user to enter the PHN of the patient to start an appointment with
        phn, ok = QInputDialog.getInt(self, "Start appointment", "Personal Health Number (PHN):")
        if ok:
            try:
                # Set the current patient in the controller
                self.controller.set_current_patient(phn)
                # Get the current patient data
                current_patient = self.controller.get_current_patient()
                # Display the patient's data
                self.show_patient_data(current_patient)
                # Proceed to the appointment menu
                self.appointment_menu()
            except IllegalAccessException:
                # Show an error if the user is not logged in
                QMessageBox.warning(self, "Error", "Must login first.")
            except IllegalOperationException:
                # Show an error if the patient is not found
                QMessageBox.warning(
                    self, "Error", f"There is no patient registered with PHN {phn}."
                )


    def appointment_menu(self):
        """
        Displays the appointment menu where the user can manage patient notes.
        """
        # Clear the central widget
        self.central_widget.deleteLater()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the appointment menu buttons
        layout = QVBoxLayout()

        # Create buttons for each appointment menu option
        self.create_note_button = QPushButton("Add note to patient record")
        self.create_note_button.clicked.connect(self.create_note)

        self.retrieve_notes_button = QPushButton("Retrieve notes from patient record by text")
        self.retrieve_notes_button.clicked.connect(self.retrieve_notes)

        self.update_note_button = QPushButton("Change note from patient record")
        self.update_note_button.clicked.connect(self.update_note)

        self.delete_note_button = QPushButton("Remove note from patient record")
        self.delete_note_button.clicked.connect(self.delete_note)

        self.list_notes_button = QPushButton("List full patient record")
        self.list_notes_button.clicked.connect(self.list_full_patient_record)

        self.end_appointment_button = QPushButton("Finish appointment")
        self.end_appointment_button.clicked.connect(self.end_appointment)

        # Add all buttons to the layout
        layout.addWidget(self.create_note_button)
        layout.addWidget(self.retrieve_notes_button)
        layout.addWidget(self.update_note_button)
        layout.addWidget(self.delete_note_button)
        layout.addWidget(self.list_notes_button)
        layout.addWidget(self.end_appointment_button)

        # Set the layout for the central widget
        self.central_widget.setLayout(layout)

    def create_note(self):
        """
        Allows the user to create a new note for the current patient.
        """
        try:
            # Prompt the user to enter the note text
            text, ok = QInputDialog.getMultiLineText(self, "Add Note", "Type the note:")
            if ok:
                # Create the note using the controller
                self.controller.create_note(text)
                # Inform the user of success
                QMessageBox.information(self, "Success", "Note added to the system.")
        except IllegalAccessException:
            # Show an error if the user is not logged in
            QMessageBox.warning(self, "Error", "Must login first.")
        except NoCurrentPatientException:
            # Show an error if there is no current patient
            QMessageBox.warning(
                self, "Error", "Cannot add a note without a valid current patient."
            )

    def retrieve_notes(self):
        """
        Retrieve notes containing a specific search string and display them in a QPlainTextEdit widget.
        """
        try:
            search_string, ok = QInputDialog.getText(self, "Retrieve Notes", "Search for:")
            if ok:
                # Retrieve matching notes
                found_notes = self.controller.retrieve_notes(search_string)
                if found_notes:
                    # Use a QPlainTextEdit to display the notes
                    text_edit = QPlainTextEdit(self)
                    text_edit.setReadOnly(True)

                    # Concatenate matching notes
                    text_content = ""
                    for note in found_notes:
                        text_content += f"Note #{note.code}, Date: {note.timestamp}\n{note.text}\n\n"

                    text_edit.setPlainText(text_content)

                    # Show the QPlainTextEdit in a dialog
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Search Results - Notes")
                    layout = QVBoxLayout()
                    layout.addWidget(text_edit)
                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "No Notes Found", f"No notes found for: {search_string}")
        except IllegalAccessException:
            QMessageBox.warning(self, "Error", "Must login first.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot retrieve notes without a valid current patient.")


    def show_notes(self, notes):
        """
        Displays a list of notes in a plain text editor within a dialog.
        """
        # Concatenate all notes into a single string
        text = ""
        for note in notes:
            text += f"Note #{note.code}, from {note.timestamp}\n{note.text}\n\n"
        # Create a dialog to display the notes
        dialog = QDialog(self)
        dialog.setWindowTitle("Notes")
        layout = QVBoxLayout()
        text_edit = QPlainTextEdit()
        text_edit.setPlainText(text)
        # Set the text editor to read-only
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        # Show the dialog
        dialog.exec()

    def update_note(self):
        """
        Allows the user to update an existing note.
        """
        try:
            # Prompt the user to enter the note number
            code, ok = QInputDialog.getInt(self, "Change Note", "Note number:")
            if ok:
                # Search for the note using the controller
                note = self.controller.search_note(code)
                if note:
                    # Display the note data
                    self.show_note_data(note)
                    # Confirm the update with the user
                    confirm = QMessageBox.question(
                        self,
                        "Confirm Update",
                        f"Are you sure you want to change note #{note.code}?",
                    )
                    if confirm == QMessageBox.StandardButton.Yes:
                        # Prompt the user to enter new text for the note
                        new_text, ok = QInputDialog.getMultiLineText(
                            self, "New Note Text", "Type new text for note:"
                        )
                        if ok:
                            # Update the note using the controller
                            self.controller.update_note(code, new_text)
                            # Inform the user of success
                            QMessageBox.information(self, "Success", "Note updated.")
                else:
                    # Show an error if the note is not found
                    QMessageBox.warning(
                        self, "Error", "There is no note registered with this number."
                    )
        except IllegalAccessException:
            # Show an error if the user is not logged in
            QMessageBox.warning(self, "Error", "Must login first.")
        except NoCurrentPatientException:
            # Show an error if there is no current patient
            QMessageBox.warning(
                self, "Error", "Cannot update note without a valid current patient."
            )

    def show_note_data(self, note):
        """
        Displays a note's data in a message box.
        """
        # Format the note's data into a string
        message = f"Note #{note.code}, from {note.timestamp}\n{note.text}"
        # Show the data in an information message box
        QMessageBox.information(self, "Note Data", message)

    def delete_note(self):
        """
        Allows the user to delete a note from the patient's record.
        """
        try:
            # Prompt the user to enter the note number
            code, ok = QInputDialog.getInt(self, "Remove Note", "Note number:")
            if ok:
                # Search for the note using the controller
                note = self.controller.search_note(code)
                if note:
                    # Display the note data
                    self.show_note_data(note)
                    # Confirm the deletion with the user
                    confirm = QMessageBox.question(
                        self,
                        "Confirm Delete",
                        f"Are you sure you want to remove note #{note.code}?",
                    )
                    if confirm == QMessageBox.StandardButton.Yes:
                        # Delete the note using the controller
                        self.controller.delete_note(code)
                        # Inform the user of success
                        QMessageBox.information(self, "Success", "Note removed.")
                else:
                    # Show an error if the note is not found
                    QMessageBox.warning(
                        self, "Error", "There is no note registered with this number."
                    )
        except IllegalAccessException:
            # Show an error if the user is not logged in
            QMessageBox.warning(self, "Error", "Must login first.")
        except NoCurrentPatientException:
            # Show an error if there is no current patient
            QMessageBox.warning(
                self, "Error", "Cannot remove note without a valid current patient."
            )

    def list_full_patient_record(self):
        """
        Lists all notes for the current patient in a QPlainTextEdit widget.
        """
        try:
            # Retrieve all notes for the current patient
            notes = self.controller.list_notes()
            if notes:
                # Create a QPlainTextEdit widget
                text_edit = QPlainTextEdit(self)
                text_edit.setReadOnly(True)

                # Concatenate all notes into a single text
                text_content = ""
                for note in notes:
                    text_content += f"Note #{note.code}, Date: {note.timestamp}\n{note.text}\n\n"

                # Set the text in the QPlainTextEdit widget
                text_edit.setPlainText(text_content)

                # Create a dialog to show the notes
                dialog = QDialog(self)
                dialog.setWindowTitle("Patient Notes")
                layout = QVBoxLayout()
                layout.addWidget(text_edit)
                dialog.setLayout(layout)
                dialog.exec()
            else:
                QMessageBox.information(self, "No Notes", "Patient record is empty.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Error", "Must login first.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot list notes without a valid current patient.")


    def end_appointment(self):
        """
        Ends the current appointment by unsetting the current patient.
        """
        try:
            # Unset the current patient using the controller
            self.controller.unset_current_patient()
            # Inform the user that the appointment has ended
            QMessageBox.information(self, "Appointment Finished", "Appointment finished.")
            # Return to the main menu
            self.main_menu()
        except IllegalAccessException:
            # Show an error if the user is not logged in
            QMessageBox.warning(self, "Error", "Must login first.")


    def logout(self):
        """
        Logs the user out of the system.
        """
        try:
            # Log out using the controller
            self.controller.logout()
            # Inform the user of success
            QMessageBox.information(self, "Logged out", "You have been logged out.")
            # Return to the login screen
            self.central_widget.deleteLater()
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.login_screen()
        except InvalidLogoutException:
            # Show an error if the user is already logged out
            QMessageBox.warning(self, "Error", "User was already logged out.")


def main():
    """
    The main function initializes the QApplication and shows the main window.
    """
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()