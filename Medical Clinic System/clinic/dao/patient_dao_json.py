from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.note import Note
import json
from clinic.patient import Patient
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

# Patient Encoder 
class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is an instance of Patient
        if isinstance(obj, Patient):
            # Return a dictionary representation of the Patient object
            return {
                "__type__": "Patient",
                "phn": obj.phn,
                "name": obj.name,
                "birth_date": obj.birth_date,
                "phone": obj.phone,
                "email": obj.email,
                "address": obj.address
            }
        # Otherwise, use the default encoding
        return super().default(obj)

# Patient Decoder
class PatientDecoder(json.JSONDecoder):
    def __init__(self, autosave=True, *args, **kwargs):
        # Save the autosave parameter to self.autosave
        self.autosave = autosave
        # Initialize the base class with the custom object_hook
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        # Check if the dictionary represents a Patient object
        if '__type__' in dct and dct['__type__'] == 'Patient':
            # Create and return a Patient object using the dictionary data
            return Patient(
                dct['phn'],
                dct['name'],
                dct['birth_date'],
                dct['phone'],
                dct['email'],
                dct['address'],
                self.autosave
            )
        # Otherwise, return the dictionary as is
        return dct

# DAO class implementation
class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave):
        # Store the autosave flag
        self.autosave = autosave
        # Set the file path for storing patient data
        self.file_path = 'clinic/patients.json'

        if autosave:
            """Initialize the patient DAO with in-memory storage and persistence."""
            # Load patients from the JSON file if autosave is enabled
            self.patients = self.load_patients()
        else:
            # Initialize an empty dictionary for patients if autosave is disabled
            self.patients = {}

    def save_patients(self):
        """Save the current patients to the JSON file."""
        with open(self.file_path, 'w') as file:
            # Serialize the patients dictionary into JSON format
            json.dump(self.patients, file, cls=PatientEncoder, indent=4)

    def load_patients(self):
        """Load patients from the JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                # Load the patients data using the custom PatientDecoder
                patients = json.load(file, cls=PatientDecoder, autosave=True)
                # Convert all keys (PHNs) to integers and return the dictionary
                return {int(k): v for k, v in patients.items()}

        # Returning empty collection if file not found or JSON decode error
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def search_patient(self, key):
        """Search for a patient by key (PHN)."""
        # Retrieve the patient from the dictionary using the key
        searched_patient = self.patients.get(key)

        # If the patient is not found, return None
        if not searched_patient:
            return None

        # Return the found patient
        return searched_patient

    def create_patient(self, patient):
        """Add a new patient."""
        # Use the patient's PHN as the key
        key = patient.phn

        # Check if a patient with the same PHN already exists
        if self.patients.get(key):
            # If so, raise an exception to prevent duplicate entries
            raise IllegalOperationException

        # Finally, create a new patient with the provided data and autosave flag
        new_patient = Patient(
            key,
            patient.name,
            patient.birth_date,
            patient.phone,
            patient.email,
            patient.address,
            self.autosave
        )
        # Add the new patient to the patients dictionary
        self.patients[key] = new_patient

        # Checking for persistence; if autosave is on, then save the collection to file
        if self.autosave:
            self.save_patients()

        # Return the newly created patient
        return new_patient

    def retrieve_patients(self, search_string):
        """Retrieve patients whose names contain the search string."""
        retrieved_patients = []
        # Iterate over all patients in the dictionary
        for patient in self.patients.values():
            # Check if the search string is in the patient's name
            if search_string in patient.name:
                # If so, add the patient to the retrieved list
                retrieved_patients.append(patient)

        # Return the list of retrieved patients
        return retrieved_patients

    def update_patient(self, original_phn, phn, name, birth_date, phone, email, address):
        """Update an existing patient's details."""
        # Retrieve the patient to be updated using the original PHN
        up_patient = self.patients.get(original_phn)
        # Set the new PHN
        new_phn = phn

        # Patient exists, update fields with new data
        up_patient.name = name
        up_patient.birth_date = birth_date
        up_patient.phone = phone
        up_patient.email = email
        up_patient.address = address

        # Treat different keys as a separate case
        if original_phn != new_phn:
            # Check if the new PHN already exists
            if self.patients.get(new_phn):
                # If so, raise an exception due to duplicate PHN
                raise IllegalOperationException
            # Remove the old entry from the dictionary
            self.patients.pop(original_phn)
            # Update the patient's PHN
            up_patient.phn = new_phn
            # Add the updated patient with the new PHN as the key
            self.patients[new_phn] = up_patient

        # Checking for persistence; if autosave is on, then save the collection to file
        if self.autosave:
            self.save_patients()

        # Return True to indicate success
        return True

    def delete_patient(self, key):
        """Remove a patient by key (PHN)."""
        # Patient exists, delete patient from the dictionary
        self.patients.pop(key)

        # Checking for persistence; if autosave is on, then save the collection to file
        if self.autosave:
            self.save_patients()

        # Return True to indicate success
        return True

    def list_patients(self):
        """List all patients."""
        patients_list = []
        # Iterate over all patients in the dictionary
        for patient in self.patients.values():
            # Add each patient to the list
            patients_list.append(patient)

        # Return the list of patients
        return patients_list
