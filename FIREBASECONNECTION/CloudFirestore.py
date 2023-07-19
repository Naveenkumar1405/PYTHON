import firebase_admin
from firebase_admin import credentials, firestore

# Replace 'path/to/serviceAccountKey.json' with the path to your downloaded service account key
cred = credentials.Certificate('./ServiceAccountKey.json')
firebase_admin.initialize_app(cred)

def add_employee_data(data):
    try:
        db = firestore.client()
        employees_collection = db.collection('Employees')
        
        # Add data to the collection
        employees_collection.add(data)
        print("Data added successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Function to read data from Firestore
def read_employee_data():
    try:
        db = firestore.client()
        employees_collection = db.collection('Employees')
        
        # Retrieve all documents in the collection
        docs = employees_collection.get()
        
        if not docs:
            print("No employee data found.")
        else:
            print("Employee data:")
            for doc in docs:
                print(f"ID: {doc.id}, Name: {doc.get('Name')}, Contact: {doc.get('Contact')}, Role: {doc.get('Role')}")
    except Exception as e:
        print(f"Error: {e}")
        
# Function to update data in Firestore
def update_employee_data(employee_id, updated_data):
    try:
        db = firestore.client()
        employees_collection = db.collection('Employees')
        
        # Update the document with the specified ID
        employees_collection.document(employee_id).update(updated_data)
        print(f"Employee data with ID '{employee_id}' updated successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Sample data to update for an employee with ID 'employee_id_to_update'
    employee_id_to_update = 'employee_id_to_update'
    updated_data = {
        'Name': 'Updated Employee Name',
        'Contact': 'Updated Contact Number',
        'Role': 'Updated Role'
    }

    update_employee_data(employee_id_to_update, updated_data)

# Function to delete data from Firestore
def delete_employee_data(employee_id):
    try:
        db = firestore.client()
        employees_collection = db.collection('Employees')
        
        # Delete the document with the specified ID
        employees_collection.document(employee_id).delete()
        print(f"Employee data with ID '{employee_id}' deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Provide the ID of the employee to delete
    employee_id_to_delete = 'employee_id_to_delete'

    delete_employee_data(employee_id_to_delete)


if __name__ == "__main__":
    # Sample data to be added
    employee_list = [
        {
            'Name': 'John Doe',
            'Contact': '1234567890',
            'Role': 'Manager'
        },
        {
            'Name': 'Jane Smith',
            'Contact': '9876543210',
            'Role': 'Developer'
        }
        # Add more employee data if needed
    ]

    # Adding the list of employees
    for employee in employee_list:
        add_employee_data(employee)
