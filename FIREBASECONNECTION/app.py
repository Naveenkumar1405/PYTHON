from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://learning-d5a85-default-rtdb.asia-southeast1.firebasedatabase.app/Employees'
})


app = Flask(__name__)

@app.route('/update_data', methods=['POST'])
def update_data():
    if request.method == 'POST':
        data = request.get_json()
        row_id = data.get('row_id')
        row_data = data.get('row_data')

        ref = db.reference('your_database_node/' + row_id)

        ref.set(row_data)

        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})


if __name__ == '__main__':
    app.run()
