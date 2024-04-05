import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Input text to be converted to speech
text = "Hello, how are you today?"

# Convert text to speech
engine.say(text)

# Wait for speech to finish
engine.runAndWait()
