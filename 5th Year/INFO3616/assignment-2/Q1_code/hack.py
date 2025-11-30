from vigenere import decrypt_vigenere
from frequency import english_freq_match_score
from english import is_english
import re
import itertools

NONLETTERS_PATTERN = re.compile('[^A-Z]')
MAX_KEY_LENGTH = 20
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SUBKEY_LETTERS_ATTEMPTS = 3

def find_repeated_substrings(string, min_len=3, max_len=5):
    # Returns a dictionary with the repeated substring as the key and a list 
    # of spacings as the value
    message = NONLETTERS_PATTERN.sub("", string.upper())

    seq_spacings = {}
    for seq_len in range(min_len, max_len + 1):
        
        # We will iterate beginning at each letter
        for seq_start in range(len(message) - seq_len + 1):
            seq = message[seq_start:seq_start + seq_len]

            # Try and find `seq` in the rest of the message
            for i in range(seq_start + seq_len, len(message) - seq_len + 1):
                if message[i:i + seq_len] == seq:
                    # Found a repeated sequence
                    if seq not in seq_spacings:
                        seq_spacings[seq] = []

                    # Save the spacing distance
                    seq_spacings[seq].append(i - seq_start)
    return seq_spacings

def get_factors(num):
    # Ignores numbers less than 2
    # Only returns factors less than MAX_KEY_LENGTH + 1

    if num < 2:
        return []

    factors = []
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
    
    return list(set(factors))

def get_most_common_factors(seq_factors):
    # Given a dictionary with sequence as key and a list of factors as value,
    # return a list of (factor, occurrences) tuples, sorted by occurrences in 
    # descending order
    factor_counts = {}
    for _, v in seq_factors.items():
        for factor in v:
            if factor not in factor_counts:
                factor_counts[factor] = 0
            factor_counts[factor] += 1
    return sorted(list(factor_counts.items()), key=lambda tup: tup[1], reverse=True)


def kasiski_examination(ciphertext):
    # 1. Find all repeated substrings in the ciphertext
    seq_spacings = find_repeated_substrings(ciphertext)

    # 2. For each substring, calculate the factors of the spacing
    seq_factors = {}
    for k, v in seq_spacings.items():
        seq_factors[k] = []
        for spacing in v:
            seq_factors[k].extend(get_factors(spacing))

    # 3. Get most common factors in descending order
    factors_by_count = get_most_common_factors(seq_factors)

    # Return likely key lengths in order of likeliness
    return [i[0] for i in factors_by_count]

def get_nth_letters_from_string(n, key_length, message):
    message = NONLETTERS_PATTERN.sub('', message.upper())

    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += key_length
    return "".join(letters)

def candidate_keys_from_scores(allFreqScores, top_k=5, limit=None):
    klen = len(allFreqScores)
    products = itertools.product(*(range(min(top_k, len(pos))) for pos in allFreqScores))
    for j, idxs in enumerate(products, start=1):
        yield ''.join(allFreqScores[i][idxs[i]][0] for i in range(klen))
        if limit and j >= limit:
            break

def attempt_hack_with_key_length(ciphertext, key_length, auto_run=False):
    # This function will get every n-th letter from the ciphertext,
    # decrypt this string 26 times (one subkey at a time),
    # and then perform frequency analysis on the decrypted string

    ciphertext_up = ciphertext.upper()

    all_freq_scores = []
    for n in range(1, key_length + 1):
        nth_letters = get_nth_letters_from_string(n, key_length, ciphertext_up)

        # Perform frequency analysis
        freq_scores = []
        for possible_subkey in LETTERS:
            decrypted_text = decrypt_vigenere(nth_letters, possible_subkey)
            score = english_freq_match_score(decrypted_text)
            tup = (possible_subkey, score)
            freq_scores.append(tup)
        
        freq_scores = sorted(freq_scores, key=lambda tup: tup[1], reverse=True)
        all_freq_scores.append(freq_scores[:SUBKEY_LETTERS_ATTEMPTS])

    # Try every combination of the most likely letters for each position
    # in the key
    best = (None, float('-inf'), None)  # (key, score, plaintext)
    for indexes in itertools.product(range(SUBKEY_LETTERS_ATTEMPTS), repeat=key_length):
        possible_key = ''
        for i in range(key_length):
            possible_key += all_freq_scores[i][indexes[i]][0]

        decrypted_text = decrypt_vigenere(ciphertext_up, possible_key)
        
        freq_match_score = english_freq_match_score(decrypted_text)
        if freq_match_score > best[1]:
            best = (possible_key, freq_match_score, decrypted_text)
        
        print(f"Possible key: {possible_key}")

        if not auto_run and is_english(decrypted_text, word_percentage=70):
            # Set the hacked ciphertext to the original casing:
            orig_case = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    orig_case.append(decrypted_text[i].upper())
                else:
                    orig_case.append(decrypted_text[i].lower())
            decrypted_text = ''.join(orig_case)

            # Check to see if the key has been found
            print(f'Possible encryption hack with key {possible_key}:')
            print(decrypted_text[:200]) 
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decrypted_text

    if auto_run and best[0] is not None:
        print(f"Best candidate key '{best[0]}' with score {best[1]:.2f}")
        print(best[2])
        return best[2]

    return None 

def hack(ciphertext, auto_run=False):
    # Perform Kasiski examination to determine the possible lengths of the
    # encryption key
    likely_key_lengths = kasiski_examination(ciphertext)

    print("Kasiski Examination: the most likely key lengths are:")
    print(likely_key_lengths)
    print()

    for key_length in likely_key_lengths:
        print(f"Attempting to decipher the message using key length {key_length}")
        result = attempt_hack_with_key_length(ciphertext, key_length, auto_run)
        if result is not None:
            return result

def main():
    with open("ciphertext.txt", "r") as f:
        ciphertext = f.read()
    
    hack(ciphertext, auto_run=False)

if __name__ == "__main__":
    main()