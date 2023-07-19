from flask import Flask, render_template, request

app = Flask(__name__)

# Replace 'mongodb://localhost:27017/' with your MongoDB connection string
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Customers']
collection = db['Client']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone_number = request.form['phoneNumber']
    location = request.form['location']

    # Create a document to insert into the MongoDB collection
    data = {"name": name, "phoneNumber": phone_number, "location": location}

    try:
        # Insert the document into the MongoDB collection
        collection.insert_one(data)
        return "Your data has been Submitted Successfully !!!"
    except Exception as e:
        return f"Failed to submit data: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
