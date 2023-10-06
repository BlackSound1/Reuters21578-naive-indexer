import json
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def main():
    # Read the naive index into memory
    with open('output/1. naive_index.txt', 'rt') as f:
        index = json.load(f)

    print(f"Initial length: {len(index)}")

    # Remove numbers
    index = remove_numbers(index)
    print(f"Length after removing numbers: {len(index)}")

    # Do case folding
    index = case_folding(index)
    print(f"Length after case folding: {len(index)}")

    # Remove 30 stopwords
    index30 = stopwords30(index)
    print(f"Length after removing 30 stopwords (from the case-folded index): {len(index30)}")

    # Remove 150 stopwords
    index150 = stopwords150(index)
    print(f"Length after removing 150 stopwords (from the case-folded index): {len(index150)}")

    # Stem
    index = stem(index150)
    print(f"Length after stemming (the index after removing 150 stopwords): {len(index)}")


def remove_numbers(index: dict) -> dict:
    # Create a new index based on the given index, keeping only non-numeric keys
    new_index = {key: val for key, val in index.items() if not key.isnumeric()}

    print("Saving to file: output/2. no_numbers_index.txt")

    with open("output/2. no_numbers_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def case_folding(index: dict) -> dict:
    # Get all the keys of the given index
    index_keys = list(index.keys())

    # Create a new index to return
    new_index = defaultdict(list)

    # Go through each of the given indexes keys
    for key in index_keys:
        lowered = key.lower()

        # Either populate or create a key based on the lower-cased version of this key.
        # The key should be associated with the postings list of that key in the original index.
        # If a postings list already exists, just append to it.
        # If it doesn't exist, the defaultdicts list for that key will be [], so can still append to it
        new_index[lowered] += index[key]

        # Sort the postings list for this key, and remove duplicates
        new_index[lowered] = sorted(set(new_index[lowered]))

    # Sort index by keys
    new_index = dict(sorted(new_index.items()))

    print("Saving to file: output/3. case_folded_index.txt")

    with open("output/3. case_folded_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def stopwords30(index: dict) -> dict:
    # Get first 30 stopwords from NLTK stopwords
    STOPWORDS = list(stopwords.words('english'))[:30]

    # Create new index based on whether the keys of the old index are stopwords
    new_index = {key: val for key, val in index.items() if key not in STOPWORDS}

    print("Saving to file: output/4a. 30_stopwords_index.txt")

    with open("output/4a. 30_stopwords_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def stopwords150(index: dict) -> dict:
    # Get first 150 stopwords from NLTK stopwords
    STOPWORDS = list(stopwords.words('english'))[:150]

    # Create new index based on whether the keys of the old index are stopwords
    new_index = {key: val for key, val in index.items() if key not in STOPWORDS}

    print("Saving to file: output/4b. 150_stopwords_index.txt")

    with open("output/4b. 150_stopwords_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def stem(index: dict) -> dict:
    # Get all the keys of the given index
    index_keys = list(index.keys())

    # Create a new index to return
    new_index = defaultdict(list)

    # Create them Porter stemmer
    stemmer = PorterStemmer()

    # Go through each of the given indexes keys
    for key in index_keys:
        stemmed = stemmer.stem(key)

        # Either populate or create a key based on the stemmed version of this key.
        # The key should be associated with the postings list of that key in the original index.
        # If a postings list already exists, just append to it.
        # If it doesn't exist, the defaultdicts list for that key will be [], so can still append to it
        new_index[stemmed] += index[key]

        # Sort the postings list for this key, and remove duplicates
        new_index[stemmed] = sorted(set(new_index[stemmed]))

    # Sort index by keys
    new_index = dict(sorted(new_index.items()))

    print("Saving to file: output/5. stemmed_index.txt")

    with open("output/5. stemmed_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


if __name__ == '__main__':
    main()
