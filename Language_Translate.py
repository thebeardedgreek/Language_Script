from googletrans import Translator, LANGUAGES

def translate_text(text, source_lang=None, dest_lang='en'):
    translator = Translator()
    try:
        if source_lang:
            translation = translator.translate(text, src=source_lang, dest=dest_lang)
        else:
            translation = translator.translate(text, dest=dest_lang)
            detected_lang_code = translator.detect(text).lang
            detected_lang = LANGUAGES.get(detected_lang_code)
            if detected_lang:
                print(f"Detected source language: {detected_lang}")
            else:
                print("Unable to detect the source language.")
        return translation.text
    except ValueError as e:
        print(f"Error: {e}")
        return None

def main():
    print("Welcome to the Text Translator!\nYou may translate to or from English with this program.\n")
    source_text = input("Enter the text you want to translate: ")
    source_lang = input("Enter the source language (leave blank for auto-detection): ")
    dest_lang = input("Enter the destination language (default is English): ")

    if not dest_lang:
        dest_lang = 'en'

    translated_text = translate_text(source_text, source_lang, dest_lang)
    if translated_text:
        print(f"\nTranslated text: {translated_text}")

if __name__ == "__main__":
    main()
