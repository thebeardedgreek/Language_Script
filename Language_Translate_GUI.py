import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES

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

# Create the main GUI window
root = tk.Tk()
root.title("Text Translator")

# Add text entry for source text
label_text = ttk.Label(root, text="Enter the text you want to translate:")
label_text.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_text = ttk.Entry(root, width=50)
entry_text.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

# Add text entry for source language
label_source_lang = ttk.Label(root, text="Enter the source language (leave blank for auto-detection):")
label_source_lang.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_source_lang = ttk.Entry(root)
entry_source_lang.grid(row=1, column=1, padx=10, pady=10)

# Add text entry for destination language
label_dest_lang = ttk.Label(root, text="Enter the destination language (default is English):")
label_dest_lang.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_dest_lang = ttk.Entry(root)
entry_dest_lang.grid(row=2, column=1, padx=10, pady=10)

# Add button to trigger translation
translate_button = ttk.Button(root, text="Translate", command=translate_text)
translate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Add label to display detected language
detected_lang_label = ttk.Label(root, text="")
detected_lang_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Add label to display translated text
translated_text_label = ttk.Label(root, text="")
translated_text_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
