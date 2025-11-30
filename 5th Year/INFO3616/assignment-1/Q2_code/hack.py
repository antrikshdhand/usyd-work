import itertools
from Crypto.Hash import MD5

MAX_LENGTH = 19
SPECIAL_CHARS = set("!@#$%^&*()_+-.?")
MAX_SPECIALS = 1

def load_dataset(path):
    hash_to_email = {}
    hashes = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            email, md5_hex = line.split(",")
            md5_hex = md5_hex.strip().lower()

            hash_to_email[md5_hex] = email.strip()
            hashes.add(md5_hex)

    return hash_to_email, hashes

def load_keywords(path):
    keywords = []
    with open(path) as f:
        for line in f:
            strip = line.strip()
            if strip:
                keywords.append(strip)

    if len(keywords) == 0:
        raise ValueError("Must have at least 1 keyword")

    return keywords

def get_md5_hex(plaintext):
    return MD5.new(plaintext.encode()).hexdigest()

def validate_candidate(cand):
    '''
    Additional rules for candidates go here.
    '''
    # Length requirement
    if len(cand) > MAX_LENGTH:
        return False

    # Special character requirement
    num_specials = 0
    for c in cand:
        if c in SPECIAL_CHARS:
            num_specials += 1
        if num_specials > MAX_SPECIALS:
            return False

    return True;

def search(hash_to_email, hashes, keywords):
    for rep in range(1, 5):
        for tup in itertools.product(keywords, repeat=rep):
            cand = "".join(tup)
            if not validate_candidate(cand):
                continue
            h = get_md5_hex(cand)
            if h in hashes:
                email = hash_to_email[h]
                return cand, h, email
    return None

def main():
    hash_to_email, hashes = load_dataset("email_md5_dataset.txt")
    keywords = load_keywords("keywords.txt")
    
    result = search(hash_to_email, hashes, keywords)
    if result:
        perm, h, email = result
        print(f"--- MATCH FOUND ---")
        print(f"Email:\t\t{email}\nPassword:\t{perm}\nMD5:\t\t{h}")
    else:
        print("No match found.")

if __name__ == "__main__":
    main()