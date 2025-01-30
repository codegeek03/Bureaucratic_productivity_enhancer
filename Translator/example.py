import os

import translator as ta


if __name__ == "__main__":
    country = "India"
    source_lang = input("Enter the source language: ")
    target_lang = input("Enter the target language: ")

    #source_text = input("Enter the text to translate: ")
    source_text = input("Enter the text to translate: ")

    translation = ta.translate(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text,
        country=country,
    )

    print(f"Translation:\n\n{translation}")