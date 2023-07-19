import nltk
from nltk.chat.util import Chat, reflections
from flask import Flask, render_template, request

# Initialize the chatbot with chatbot pairs
pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!",]
    ],
    [
        r"how can I (.*)",
        ["You can %1 by doing XYZ.", "To %1, you need to follow these steps: ...",]
    ],
    [
        r"what can you do",
        ["I can answer questions, provide information, and have casual conversations.",]
    ],
    [
        r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!", 
         "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",]
    ],
    [
        r"what is your favorite food?",
        ["As an AI, I don't eat, but I'd say data and algorithms are quite tasty.",]
    ],
    [
        r"who created you|who is your creator",
        ["I was created by an awesome team of developers.",]
    ],
    [
        r"help",
        ["Sure, I'm here to help! What do you need assistance with?",]
    ],
    [
        r"(.*) (love|like) you",
        ["Aww, that's sweet of you to say!", "Thanks! I appreciate it.",]
    ],
    [
        r"what is the weather today?",
        ["I'm sorry, I can't provide real-time data, but you can check a weather website or app.",]
    ],
    [
        r"who am I",
        ["I'm sorry, I don't have access to personal information. Could you tell me more about yourself?",]
    ],
    [
        r"what is the meaning of life?",
        ["The meaning of life is a complex philosophical question with no definitive answer.",]
    ],
    [
        r"where are you from?",
        ["I'm an AI language model, so I don't have a physical location.",]
    ],
    [
        r"what is the capital of (.*)",
        ["The capital of %1 is XYZ.",]
    ],
    [
        r"tell me a fun fact",
        ["Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs still perfectly edible!", 
         "Bananas are berries, but strawberries are not.",]
    ],
    [
        r"thank you",
        ["You're welcome!", "No problem! If you have any more questions, feel free to ask.",]
    ],
    [
        r"my name is (.*)",
        ["Hello %1, How can I assist you today?",]
    ],
    [
        r"what is your name?",
        ["You can call me Wolfie.",]
    ],
    [
        r"how are you?",
        ["I'm doing well, thank you!", "I'm fine, thanks!",]
    ],
    [
        r"exit",
        ["ChatBot: Goodbye!",]
    ],
    [
        r"(.*)",
        ["Sorry, I can't understand that. Please ask something else.",]
    ]
]

chatbot = Chat(pairs, reflections)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"].lower()
    if user_input == "exit":
        response = "ChatBot: Goodbye!"
    else:
        response = chatbot.respond(user_input)
    return response

if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
    app.run(port=8080, debug=True)


