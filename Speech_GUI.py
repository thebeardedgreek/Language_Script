import os
import pyttsx3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

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

def list_available_voices():
    available_voices = []
    for voice in voices:
        available_voices.append(voice.name)
    return available_voices

def set_language(language):
    engine.setProperty('language', language)

def set_voice(voice):
    engine.setProperty('voice', voice)

def set_speech_effects(rate, volume):
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

def save_audio(text, filename):
    directory = "Saved Audios"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename_with_extension = f"{filename}.mp3"
    engine.save_to_file(text, os.path.join(directory, filename_with_extension))
    engine.runAndWait()

def repeat_text(text, repeat):
    for _ in range(repeat):
        engine.say(text)
        engine.runAndWait()

def on_submit():
    text = entry_text.get()
    voice = combo_voice.get()
    rate = float(entry_rate.get())
    volume = float(entry_volume.get()) / 10  # Scale the volume level to be between 0.1 and 1.0
    filename = entry_filename.get()

    set_voice(voice)
    set_speech_effects(rate, volume)

    repeat_choice = messagebox.askyesno("Repeat Text", "Would you like to repeat the text?")
    if repeat_choice:
        repeat = int(entry_repeat.get())
        repeat_text(text, repeat)
    else:
        engine.say(text)
        engine.runAndWait()

    save_choice = messagebox.askyesno("Save Audio", "Would you like to save the audio?")
    if save_choice:
        save_audio(text, filename)

# Create the GUI
root = tk.Tk()
root.title("Text-to-Speech Customizer")

# Padding between the words and selection areas and the sides of the GUI
pad_x = 20
pad_y = (10, 5)

label_text = tk.Label(root, text="Enter the text:")
label_text.grid(row=0, column=0, sticky="w", padx=pad_x, pady=pad_y)
entry_text = tk.Entry(root, width=50)
entry_text.grid(row=0, column=1, columnspan=2, padx=pad_x, pady=pad_y)

# Check if there are available languages
languages = list_available_languages()
if languages:
    label_language = tk.Label(root, text="Choose language:")
    label_language.grid(row=1, column=0, sticky="w", padx=pad_x, pady=pad_y)
    combo_language = ttk.Combobox(root, values=languages)
    combo_language.grid(row=1, column=1, padx=pad_x, pady=pad_y)

label_voice = tk.Label(root, text="Choose voice:")
label_voice.grid(row=2, column=0, sticky="w", padx=pad_x, pady=pad_y)
voices = list_available_voices()
combo_voice = ttk.Combobox(root, values=voices)
combo_voice.grid(row=2, column=1, padx=pad_x, pady=pad_y)

label_rate = tk.Label(root, text="Enter speech rate (words per minute):")
label_rate.grid(row=3, column=0, sticky="w", padx=pad_x, pady=pad_y)
entry_rate = tk.Entry(root)
entry_rate.grid(row=3, column=1, padx=pad_x, pady=pad_y)

label_volume = tk.Label(root, text="Enter volume level (1 to 10):")
label_volume.grid(row=4, column=0, sticky="w", padx=pad_x, pady=pad_y)
entry_volume = tk.Entry(root)
entry_volume.grid(row=4, column=1, padx=pad_x, pady=pad_y)

label_filename = tk.Label(root, text="Enter filename (without extension):")
label_filename.grid(row=5, column=0, sticky="w", padx=pad_x, pady=pad_y)
entry_filename = tk.Entry(root)
entry_filename.grid(row=5, column=1, padx=pad_x, pady=pad_y)

label_repeat = tk.Label(root, text="Enter the number of times to repeat:")
label_repeat.grid(row=6, column=0, sticky="w", padx=pad_x, pady=pad_y)
entry_repeat = tk.Entry(root)
entry_repeat.grid(row=6, column=1, padx=pad_x, pady=pad_y)

button_submit = tk.Button(root, text="Submit", command=on_submit)
button_submit.grid(row=7, column=0, columnspan=2, padx=pad_x, pady=pad_y)

root.mainloop()
