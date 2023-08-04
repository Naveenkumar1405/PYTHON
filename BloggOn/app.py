from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
import bcrypt
import random
import string
from flask_mail import Mail, Message
from pymongo.errors import ConnectionFailure
from gridfs import GridFS
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from flask_pymongo import PyMongo
import base64
from bson.objectid import ObjectId
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'navinmano1412@gmail.com'
app.config['MAIL_PASSWORD'] = 'naadtcvzyppgtrzm'
app.config['UPLOAD_FOLDER'] = 'static/img'

mail = Mail(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['BloggOn']
collection = db['Users']
fs = GridFS(db)
users = db['Users']
blogs = db['Blogs']
media = db['Media']
app.config['MONGO_URI'] = 'mongodb://localhost:27017/BloggOn'
mongo = PyMongo(app)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class Media:
    def __init__(self, email, filename):
        self.email = email
        self.filename = filename

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

class User:
    def __init__(self, name, email, profile_pic):
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def get_media_files(self):
        media_files = db.media_files.find({"email": self.email})
        return media_files

    def get_email(self):
        return self.email

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('homepage'))
    return render_template('homepage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        existing_user = collection.find_one({"email": email})
        if existing_user:
            flash("Email already exists. Please sign in.")
            return redirect(url_for('signin'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        data = {"name": name, "password": hashed_password, "email": email}

        try:
            collection.insert_one(data)
            flash("Registration successful! Please sign in with your new account.")
            return redirect(url_for('signin'))
        except Exception as e:
            return f"Failed to submit data: {str(e)}", 500
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({"name": username})
        password_from_db = user['password']
        if user and bcrypt.checkpw(password.encode('utf-8'), password_from_db):
            session['email'] = user['email']
            return redirect(url_for('homepage'))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = collection.find_one({"email": email})
        if user:
            otp = generate_otp()
            collection.update_one({"_id": user['_id']}, {"$set": {"otp": otp}})
            msg = Message('OTP for Login', sender='your_gmail_username', recipients=[email])
            msg.body = f'Login to your BloggOn Account using: {otp}'
            mail.send(msg)
            return "OTP has been sent to your email address. Please check your inbox."
        return "Email not found in the database. Please check the entered email."
    return redirect(url_for('signin'))

@app.route('/signout')
def signout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        email = request.form['email']
        otp_entered = request.form['otp']
        user = collection.find_one({"email": email, "otp": otp_entered})
        if user:
            collection.update_one({"email": email}, {"$unset": {"otp": ""}})
            return "OTP verification successful."
        return "Invalid OTP. Please try again."
    return redirect(url_for('signin'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'email' not in session:
        return redirect(url_for('signin'))
    email = session['email']
    user_data = collection.find_one({"email": email})
    if user_data:
        existing_profile_pic_b64 = user_data.get("profile_pic")
        if request.method == 'POST':
            name = request.form['name']
            bio = request.form['bio']
            social_media_links = request.form['social_media_links']
            profile_pic = request.files['profile_pic']
            profile_pic_b64 = None 
            if profile_pic:
                image_binary = profile_pic.read()
                profile_pic_b64 = base64.b64encode(image_binary).decode('utf-8')
            else:
                profile_pic_b64 = existing_profile_pic_b64
            collection.update_one({"email": email}, {
                "$set": {
                    "name": name,
                    "bio": bio,
                    "social_media_links": social_media_links,
                    "profile_pic": profile_pic_b64 
                }
            })
            flash("Profile updated successfully!", "success")
            return redirect(url_for('account'))
        return render_template('account.html', user_data=user_data, existing_profile_pic_b64=existing_profile_pic_b64)
    else:
        return "User not found."

@app.route('/homepage')
def homepage():
    blogs = db.Blogs.find()
    
    blogs_list = [blog for blog in blogs]
    
    email = session.get('email')
    blogs_list = deque(db['Blogs'].find({}))
    blogs_list.reverse()
    if email:
        current_user_media = db.media.find({"email": email})
        return render_template('homepage.html', media_files=current_user_media,blogs_list=blogs_list)
    else:
        return render_template('homepage.html', media_files=None, blogs_list=blogs_list)


@app.route('/blog/<blog_id>', methods=['GET', 'POST'])
def blog_article(blog_id):
    blog = blogs.find_one({"_id": ObjectId(blog_id)})
    if blog:
        if request.method == 'POST':
            if 'like_btn' in request.form:
                blogs.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"likes": 1}})
                blog = blogs.find_one({"_id": ObjectId(blog_id)})
                return jsonify({"likes": blog['likes']})
            elif 'comment_btn' in request.form:
                comment_text = request.form['comment']
                if comment_text:
                    blogs.update_one({"_id": ObjectId(blog_id)}, {"$push": {"comments": comment_text}})
                    blog = blogs.find_one({"_id": ObjectId(blog_id)})
                    return jsonify({"comments": blog['comments']})
            elif 'bookmark_btn' in request.form:
                blogs.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"bookmarks": 1}})
                blog = blogs.find_one({"_id": ObjectId(blog_id)})
                return jsonify({"bookmarks": blog['bookmarks']})
        return render_template('blog_article.html', blog=blog)
    else:
        return "Blog not found." 
    
@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if 'email' not in session:
        return redirect(url_for('signin'))
    if request.method == 'POST':
        email = session['email']
        user_data = users.find_one({"email": email})
        if user_data:
            title = request.form['title']
            description = request.form['description']
            blog_text = request.form['blog_text']
            blog_entry = {
                "email": email, 
                "title": title,
                "description": description,
                "blog_text": blog_text
            }
            blogs.insert_one(blog_entry)
            flash("Blog article created successfully!", "success")
            return redirect(url_for('homepage'))
    return render_template('create_blog.html')
    
@app.route('/update_password', methods=['POST'])
def update_password():
    if 'email' not in session:
        return jsonify({"message": "User not authenticated."}), 401
    email = session['email']
    user_data = collection.find_one({"email": email}) 
    if user_data:
        if request.method == 'POST':
            new_password = request.json.get('password')
            if new_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                collection.update_one({"email": email}, { 
                    "$set": {
                        "password": hashed_password
                    }
                })
                return jsonify({"message": "Password updated successfully."}), 200
            else:
                return jsonify({"message": "Invalid request. New password not provided."}), 400
        else:
            return jsonify({"message": "Invalid request method."}), 400
    else:
        return jsonify({"message": "User not found."}), 404
          
if __name__ == '__main__':
    app.run(debug=True, port=8000)
