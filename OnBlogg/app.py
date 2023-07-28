from flask import Flask, jsonify

app = Flask(__name__)

blog_posts = [
    {
        'title': 'Introduction to Mathematics',
        'content': 'Mathematics is the language of science...',
        'author': 'John Doe',
        'date': '2023-07-24'
    },
    {
        'title': 'History of Ancient Civilizations',
        'content': 'Ancient civilizations laid the foundation...',
        'author': 'Jane Smith',
        'date': '2023-07-23'
    }
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify({'posts': blog_posts})

if __name__ == '__main__':
    app.run(debug=True)
