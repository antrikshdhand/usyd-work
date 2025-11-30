import json
import re

NONLETTERS_BUT_KEEP_SPACE = re.compile(r'[^A-Z\s]')

def load_dictionary():
    with open("words_dictionary.json") as f:
        data = json.load(f)
    return {w.upper() for w in data.keys()}

ENGLISH_WORDS = load_dictionary()

def remove_non_letters(message):
    return NONLETTERS_BUT_KEEP_SPACE.sub("", message.upper())

def get_english_words_percentage(message):
    msg = message.upper()
    cleaned = remove_non_letters(msg)
    possible_words = cleaned.split()
    if possible_words == []:
        return 0.0

    matches = sum(1 for w in possible_words if w in ENGLISH_WORDS)
    return (matches / len(possible_words)) * 100.0

def get_letters_percentage(message):
    allowed = sum(1 for ch in message if ch.isalpha() or ch.isspace())
    return (allowed / len(message)) * 100.0

def is_english(message, word_percentage=20, letter_percentage=85):
    # By default, 20% of the words must exist in the dictionary file, and
    # 85% of all the characters in the message must be letters or spaces
    # (not punctuation or numbers).
    words_match = get_english_words_percentage(message) >= word_percentage
    letters_match = get_letters_percentage(message) >= letter_percentage
    return words_match and letters_match