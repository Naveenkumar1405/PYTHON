import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Replace with your Firebase project credentials JSON file path
cred = credentials.Certificate("./ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

def sort_and_push_to_firebase(excel_file_path, collection_name):
    # Read data from Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)

    # Sort the DataFrame by the 'Name' column
    df = df.sort_values(by='Name')

    # Convert the DataFrame to a list of dictionaries (JSON-like format)
    data_to_push = df.to_dict(orient='records')

    # Initialize a Firestore client
    db = firestore.client()

    # Push data to the specified collection in Firebase
    for data in data_to_push:
        db.collection(collection_name).update(data)

    print("Data has been sorted and pushed to Firebase successfully.")

if __name__ == "__main__":
    # Replace with your Excel file path and the desired collection name in Firebase
    excel_file_path = "CUSTOMERDATA.xlsx"
    collection_name = "customers"

    sort_and_push_to_firebase(excel_file_path, collection_name)
