import speech_recognition as sr
import pyttsx3
import re

# Initialize recognizer and voice engine
r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Sam:", text)  # Print for clarity
    engine.say(text)
    engine.runAndWait()

def calculate(command):
    command = command.lower()

    # Replace words with symbols
    command = command.replace("plus", "+").replace("add", "+")
    command = command.replace("minus", "-").replace("subtract", "-")
    command = command.replace("times", "*").replace("multiply", "*")
    command = command.replace("divide", "/").replace("over", "/")

    # Remove filler words
    expr = re.sub(r"sam|what is|calculate|equals|by|and", "", command).strip()

    try:
        result = eval(expr)
        return result
    except:
        return None

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            return command
        except:
            return ""

# Main loop
while True:
    command = listen()
    if command.lower().startswith("sam"):
        speak("Yes, I am listening")
        command = listen()  # Listen for the actual math command
        print("You said:", command)
        result = calculate(command)
        if result is not None:
            speak(f"The result is {result}")
        else:
            speak("Sorry, I couldn’t calculate that.")
