# Six most frequent letters in English are E, T, A, O, I, N
# Six least frequent letters in English are V, K, J, X , Q, Z
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_letter_count(string):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message
    letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0,
        'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0,
        'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0,
        'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in string.upper():
        if letter in LETTERS:
            letter_count[letter] += 1
    
    return letter_count 

def get_frequency_order(string):
    letter_to_freq = get_letter_count(string)

    # Now we want to convert this into a dictionary with frequency as key
    # and a list of letters with that frequency as value
    freq_to_letter = {}
    for k, v in letter_to_freq.items():
        if v not in freq_to_letter:
            freq_to_letter[v] = []
        freq_to_letter[v].append(k)

    # Sort the lists of letters in reverse ETAOIN order to prevent over-counting
    for k, v in freq_to_letter.items():
        freq_to_letter[k].sort(key=ETAOIN.find, reverse=True)

        # Convert into string
        freq_to_letter[k] = "".join(freq_to_letter[k])

    # Get a list of strings in descending order of frequency
    letters = []
    for freq in sorted(freq_to_letter.keys(), reverse=True):
        letters.append(freq_to_letter[freq])

    return "".join(letters)

def english_freq_match_score(string):
    # We will calculate a "frequency match score" for a given string
    # 1. Order the letters in the string by highest frequency to lowest frequency
    # 2. For each of the six most frequent letters in the string, if they are also 
    # one of the six most frequent letters in English, then we add 1
    # 3. Repeat for the six least frequent letters in the string.
    # Hence, the frequency match schore for a string can range from 0 to 12.

    ordered_str = get_frequency_order(string)

    score = 0
    for common_chr in ETAOIN[:6]:
        if common_chr in ordered_str[:6]:
            score += 1
    for uncommon_chr in ETAOIN[-6:]:
        if uncommon_chr in ordered_str[-6:]:
            score += 1
    
    return score