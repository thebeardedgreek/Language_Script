import os
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

def list_available_languages():
    """
    Collects and returns available languages from the available voices.
    """
    available_languages = set()
    for voice in voices:
        languages = voice.languages
        if languages:
            available_languages.update(languages)
    return available_languages

def list_available_voices():
    """
    Lists available voices along with their indices.
    """
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i + 1}. {voice.name}")

def set_language():
    """
    Prompts the user to choose a language and sets the text-to-speech engine to use the chosen language.
    """
    available_languages = list_available_languages()
    if available_languages:
        print("Available languages:")
        for i, language in enumerate(available_languages):
            print(f"{i + 1}. {language}")
        
        while True:
            try:
                choice = int(input("Enter the number corresponding to the language you want to use: "))
                if 0 < choice <= len(available_languages):
                    chosen_language = list(available_languages)[choice - 1]
                    engine.setProperty('language', chosen_language)
                    break
                else:
                    print("Invalid choice. Please choose a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    else:
        print("There are no alternative languages available to be used on this machine.")

def set_voice():
    """
    Prompts the user to choose a voice and sets the text-to-speech engine to use the chosen voice.
    """
    list_available_voices()
    while True:
        try:
            choice = int(input("Enter the number corresponding to the voice you want to use: "))
            if 0 < choice <= len(voices):
                chosen_voice_id = voices[choice - 1].id
                engine.setProperty('voice', chosen_voice_id)
                break
            else:
                print("Invalid choice. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def set_speech_effects():
    """
    Prompts the user to set speech rate and volume level.
    """
    while True:
        try:
            rate = float(input("Enter speech rate (words per minute): "))
            engine.setProperty('rate', rate)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for speech rate.")

    while True:
        try:
            volume = float(input("Enter volume level (0.0 to 1.0): "))
            if 0.0 <= volume <= 1.0:
                engine.setProperty('volume', volume)
                break
            else:
                print("Invalid input. Please enter a number between 0.0 and 1.0 for volume level.")
        except ValueError:
            print("Invalid input. Please enter a valid number for volume level.")


def save_audio(text, filename=None):
    """
    Saves the text-to-speech output as an audio file with the specified filename and format.
    """
    directory = "Saved Audios"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if filename is None:
        while True:
            filename = input("Enter filename (without extension): ")
            if filename.strip():  # Check if filename is not empty
                break
            else:
                print("Filename cannot be empty. Please enter a valid filename.")
        
        while True:
            output_format = input("Enter audio file format (e.g., mp3, wav): ")
            if output_format.lower() in ['mp3', 'wav']:
                break
            else:
                print("Invalid audio file format. Please enter 'mp3' or 'wav'.")
        
        filename_with_extension = f"{filename}.{output_format}"
        engine.save_to_file(text, os.path.join(directory, filename_with_extension))
        engine.runAndWait()
    else:
        engine.save_to_file(text, os.path.join(directory, filename))
        engine.runAndWait()

def repeat_text(text, repeat):
    """
    Repeats the text-to-speech output for the specified number of times.
    """
    for _ in range(repeat):
        engine.say(text)
        engine.runAndWait()

# Prompt user to customize text-to-speech settings
print("Welcome to the Text-to-Speech Customizer!")
set_language()
set_voice()
set_speech_effects()

# Prompt user for the text to be spoken
while True:
    try:
        text = input("Enter the text you want to be spoken aloud: ")
        if text.strip():  # Check if text is not empty
            break
        else:
            print("Text cannot be empty. Please enter some text.")
    except ValueError:
        print("Invalid input. Please enter some text.")

# Ask if user wants to repeat the text
while True:
    repeat_choice = input("Would you like to repeat the text? (y/n): ")
    if repeat_choice.lower() in ['y', 'n']:
        break
    else:
        print("Invalid choice. Please enter 'y' or 'n'.")

if repeat_choice.lower() == 'y':
    while True:
        try:
            repeat = int(input("Enter the number of times to repeat: "))
            if repeat > 0:
                break
            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    repeat_text(text, repeat)
else:
    # Convert text to speech
    engine.say(text)
    engine.runAndWait()

# Options after speech is given
while True:
    try:
        option = int(input("Options:\n1. Save audio to file\n2. Speak another text\n3. Quit\nChoose an option (1/2/3): "))
        if option == 1:
            save_audio(text)
            break
        elif option == 2:
            reset_choices = input("Would you like to change the settings of the speech to text? (y/n) ")
            while reset_choices.lower() not in ['y', 'n']:
                print("Invalid choice. Please enter 'y' or 'n'.")
                reset_choices = input("Would you like to change the settings of the speech to text? (y/n) ")
            
            if reset_choices.lower() == 'y':
                engine.stop()  # Stop the current speech
                # Reset settings for new text
                set_language()
                set_voice()
                set_speech_effects()
                text = input("Enter the text you want to be spoken aloud: ")
                repeat_choice = input("Would you like to repeat the text? (y/n): ")
                if repeat_choice.lower() == 'y':
                    repeat = int(input("Enter the number of times to repeat: "))
                    repeat_text(text, repeat)
                else:
                    engine.say(text)
                    engine.runAndWait()
            else:
                text = input("Enter the text you want to be spoken aloud: ")
                repeat_choice = input("Would you like to repeat the text? (y/n): ")
                if repeat_choice.lower() == 'y':
                    repeat = int(input("Enter the number of times to repeat: "))
                    repeat_text(text, repeat)
                else:
                    engine.say(text)
                    engine.runAndWait()
        elif option == 3:
            break
        else:
            print("Invalid choice. Please choose a number from the list.")
    except ValueError:
        print("Invalid input. Please enter a number.")

