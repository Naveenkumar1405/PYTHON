import snowboydecoder
import sys

# Replace 'path_to_your_model.pmdl' with the actual path to your downloaded model file.
# You can provide multiple model files to detect multiple wake words.
models = ["path_to_your_model.pmdl"]

def detected_callback():
    print("Wake word detected!")  # You can perform any action here when the wake word is detected.
    # For example, trigger Alexa functionality or any other custom action.

def interrupt_callback():
    return False

# Initialize Snowboy detector
detector = snowboydecoder.HotwordDetector(models, sensitivity=0.5)

print("Listening... Press Ctrl+C to exit.")

# Start the wake word detection
detector.start(detected_callback=detected_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()  # Clean up the detector when done.
