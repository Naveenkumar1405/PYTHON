import firebase_admin
from firebase_admin import credentials, db

# Replace 'path/to/serviceAccountKey.json' with the path to your downloaded service account key
cred = credentials.Certificate('./ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://learning-d5a85-default-rtdb.asia-southeast1.firebasedatabase.app/Employees'  # Replace 'your-project-id' with your Firebase project ID
})

def add_employee_data(data):
    try:
        ref = db.reference('Employees')
        ref.push(data)
        print("Data added successfully!")
    except Exception as e:
        print(f"Error: {e}")
        
def read_employee_data():
    try:
        ref = db.reference('Employees')
        snapshot = ref.get()
        
        if snapshot:
            # If data is available in the snapshot
            print("Employee data:")
            for key, value in snapshot.items():
                print(f"ID: {key}, Name: {value['Name']}, Contact: {value['Contact']}, Role: {value['Role']}")
        else:
            print("No employee data found.")
    except Exception as e:
        print(f"Error: {e}")
        
# Function to update data in Firebase
def update_employee_data(employee_id, updated_data):
    try:
        ref = db.reference('Employees')
        employee_ref = ref.child(employee_id)

        employee_ref.update(updated_data)
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

# Function to delete data from Firebase
def delete_employee_data(employee_id):
    try:
        ref = db.reference('Employees')
        employee_ref = ref.child(employee_id)

        employee_ref.delete()
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
