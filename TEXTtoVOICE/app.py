from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)

    # Specify the path to the existing "static" directory
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

    # Ensure the "static" directory exists and create it if not
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    audio_file = os.path.join(static_dir, 'audio.mp3')
    myobj.save(audio_file)
    os.system("mpg321 " + audio_file)

    # Delete the audio file after playing
    os.remove(audio_file)

    return jsonify({'message': 'Audio playback complete!'})

if __name__ == '__main__':
    app.run(debug=True)
