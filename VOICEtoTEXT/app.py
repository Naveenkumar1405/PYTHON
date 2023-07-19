from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

# Global variables to track audio processing
recognizer = sr.Recognizer()
stop_listening = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded.'})

    audio = request.files['audio']
    text = transcribe_audio(audio)

    return jsonify({'text': text})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_listening
    if stop_listening:
        stop_listening()

    return jsonify({'message': 'Audio processing stopped.'})

def transcribe_audio(audio):
    global stop_listening
    stop_listening = None

    def callback(recognizer, audio_data):
        global stop_listening
        try:
            text = recognizer.recognize_google(audio_data)
            print("Recognized Text:", text)
            # Perform any desired processing with the recognized text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    stop_listening = recognizer.listen_in_background(sr.AudioFile(audio), callback)

    return "Audio processing started."

if __name__ == '__main__':
    app.run()
