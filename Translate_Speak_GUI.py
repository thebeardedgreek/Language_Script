import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES
import pyttsx3
import os
from tkinter import messagebox

# Initialize the text-to-speech engine
engine = pyttsx3.init()
# Get available voices
voices = engine.getProperty('voices')

# Function to list available languages based on available voices
def list_available_languages():
    available_languages = set()
    for voice in voices:
        languages = voice.languages
        if languages:
            available_languages.update(languages)
    if available_languages:
        return available_languages
    else:
        return None

# Function to list available voices
def list_available_voices():
    available_voices = []
    for voice in voices:
        available_voices.append(voice.name)
    return available_voices

# Function to set the language for text-to-speech
def set_language(language):
    engine.setProperty('language', language)

# Function to set the voice for text-to-speech
def set_voice(voice):
    engine.setProperty('voice', voice)

# Function to set speech effects such as rate and volume
def set_speech_effects(rate, volume):
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

# Function to save audio to file
def save_audio(text, filename):
    directory = "Saved Audios"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename_with_extension = f"{filename}.mp3"
    engine.save_to_file(text, os.path.join(directory, filename_with_extension))
    engine.runAndWait()

# Function to repeat text for specified number of times
def repeat_text(text, repeat):
    for _ in range(repeat):
        engine.say(text)
        engine.runAndWait()

# Function to handle submit button click event
def on_submit():
    text = entry_text.get()
    voice = combo_voice.get()
    rate = float(entry_rate.get())
    volume = float(entry_volume.get()) / 10  # Scale the volume level to be between 0.1 and 1.0
    filename = entry_filename.get()

    set_voice(voice)
    set_speech_effects(rate, volume)

    # Ask user if they want to repeat the text
    repeat_choice = messagebox.askyesno("Repeat Text", "Would you like to repeat the text?")
    if repeat_choice:
        repeat = int(entry_repeat.get())
        repeat_text(text, repeat)
    else:
        engine.say(text)
        engine.runAndWait()

    # Ask user if they want to save the audio
    save_choice = messagebox.askyesno("Save Audio", "Would you like to save the audio?")
    if save_choice:
        save_audio(text, filename)

# Function to translate text
def translate_text():
    source_text = entry_text.get()
    source_lang = entry_source_lang.get()
    dest_lang = entry_dest_lang.get() if entry_dest_lang.get() else 'en'

    translator = Translator()
    try:
        if source_lang:
            translation = translator.translate(source_text, src=source_lang, dest=dest_lang)
        else:
            translation = translator.translate(source_text, dest=dest_lang)
            detected_lang_code = translator.detect(source_text).lang
            detected_lang = LANGUAGES.get(detected_lang_code)
            if detected_lang:
                detected_lang_label.config(text=f"Detected source language: {detected_lang}")
            else:
                detected_lang_label.config(text="Unable to detect the source language.")
        translated_text_label.config(text=f"Translated text: {translation.text}")
    except ValueError as e:
        translated_text_label.config(text=f"Error: {e}")

# Function to open the text-to-speech customization window
def open_text_to_speech():
    tts_window = tk.Toplevel()
    tts_window.title("Text-to-Speech Customizer")

    # Padding between the words and selection areas and the sides of the GUI
    pad_x = 20
    pad_y = (10, 5)

    label_text = tk.Label(tts_window, text="Enter the text:")
    label_text.grid(row=0, column=0, sticky="w", padx=pad_x, pady=pad_y)
    entry_text = tk.Entry(tts_window, width=50)
    entry_text.grid(row=0, column=1, columnspan=2, padx=pad_x, pady=pad_y)

    # Check if there are available languages
    languages = list_available_languages()
    if languages:
        label_language = tk.Label(tts_window, text="Choose language:")
        label_language.grid(row=1, column=0, sticky="w", padx=pad_x, pady=pad_y)
        combo_language = ttk.Combobox(tts_window, values=languages)
        combo_language.grid(row=1, column=1, padx=pad_x, pady=pad_y)

    label_voice = tk.Label(tts_window, text="Choose voice:")
    label_voice.grid(row=2, column=0, sticky="w", padx=pad_x, pady=pad_y)
    voices = list_available_voices()
    combo_voice = ttk.Combobox(tts_window, values=voices)
    combo_voice.grid(row=2, column=1, padx=pad_x, pady=pad_y)

    label_rate = tk.Label(tts_window, text="Enter speech rate (words per minute):")
    label_rate.grid(row=3, column=0, sticky="w", padx=pad_x, pady=pad_y)
    entry_rate = tk.Entry(tts_window)
    entry_rate.grid(row=3, column=1, padx=pad_x, pady=pad_y)

    label_volume = tk.Label(tts_window, text="Enter volume level (1 to 10):")
    label_volume.grid(row=4, column=0, sticky="w", padx=pad_x, pady=pad_y)
    entry_volume = tk.Entry(tts_window)
    entry_volume.grid(row=4, column=1, padx=pad_x, pady=pad_y)

    label_filename = tk.Label(tts_window, text="Enter filename (without extension):")
    label_filename.grid(row=5, column=0, sticky="w", padx=pad_x, pady=pad_y)
    entry_filename = tk.Entry(tts_window)
    entry_filename.grid(row=5, column=1, padx=pad_x, pady=pad_y)

    label_repeat = tk.Label(tts_window, text="Enter the number of times to repeat:")
    label_repeat.grid(row=6, column=0, sticky="w", padx=pad_x, pady=pad_y)
    entry_repeat = tk.Entry(tts_window)
    entry_repeat.grid(row=6, column=1, padx=pad_x, pady=pad_y)

    button_submit = tk.Button(tts_window, text="Submit", command=on_submit)
    button_submit.grid(row=7, column=0, columnspan=2, padx=pad_x, pady=pad_y)

    # Make window resizable and expand widgets with window resizing
    tts_window.columnconfigure((0, 1), weight=1)  # Make both columns expand equally
    tts_window.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)  # Make these rows expand equally

# Function to open the text translator window
def open_text_translator():
    translator_window = tk.Toplevel()
    translator_window.title("Text Translator")

    label_text = ttk.Label(translator_window, text="Enter the text you want to translate:")
    label_text.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_text = ttk.Entry(translator_window, width=50)
    entry_text.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
    
    label_source_lang = ttk.Label(translator_window, text="Enter the source language (leave blank for auto-detection):")
    label_source_lang.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_source_lang = ttk.Entry(translator_window)
    entry_source_lang.grid(row=1, column=1, padx=10, pady=10)
    
    label_dest_lang = ttk.Label(translator_window, text="Enter the destination language (default is English):")
    label_dest_lang.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_dest_lang = ttk.Entry(translator_window)
    entry_dest_lang.grid(row=2, column=1, padx=10, pady=10)

    translate_button = ttk.Button(translator_window, text="Translate", command=translate_text)
    translate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    global detected_lang_label
    detected_lang_label = ttk.Label(translator_window, text="")
    detected_lang_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    global translated_text_label
    translated_text_label = ttk.Label(translator_window, text="")
    translated_text_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Make window resizable and expand widgets with window resizing
    translator_window.columnconfigure((0, 1), weight=1)  # Make both columns expand equally
    translator_window.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)  # Make these rows expand equally

# Create the main GUI window
root = tk.Tk()
root.title("Main Menu")
root.geometry("400x100")

# Add button to open text-to-speech customization window
tts_button = ttk.Button(root, text="Text-to-Speech Customization", command=open_text_to_speech)
tts_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Use sticky="ew" to make the button expand horizontally with window resizing

# Add button to open text translator window
translator_button = ttk.Button(root, text="Text Translator", command=open_text_translator)
translator_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # Use sticky="ew" to make the button expand horizontally with window resizing

# Set column and row weights to make the buttons expand with window resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
