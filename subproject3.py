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

    # # Stem
    # index = stem(index150)
    # print(f"Length after stemming (the index after removing 150 stopwords): {len(index)}")


def remove_numbers(index: dict) -> dict:
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
        # Either populate or create a key based on the lower-cased version of this key.
        # The key should be associated with the postings list of that key in the original index.
        # If a postings list already exists, just append to it.
        # If it doesn't exist, the defaultdicts list for that key will be [], so can still append to it
        new_index[key.lower()] += index[key]

        # Sort the postings list for this key, and remove duplicates
        new_index[key.lower()] = sorted(set(new_index[key.lower()]))

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
    index_keys = index.keys()

    # Create them Porter stemmer
    stemmer = PorterStemmer()

    new_index = defaultdict(list)

    # Create a tuple of keys that are similar, where similar means of the same word type, considering stemming
    similar_keys = set()

    # For each of the keys in the index, associate members of the same word type and put them in the similar_keys set
    print("Making a set of tuples. Each tuple contains all versions of a word type, considering stemming."
          " This will take a while...")
    for key in index_keys:
        similar = tuple(k for k in index_keys if stemmer.stem(k) == stemmer.stem(key))
        similar_keys.add(similar)

    # Navigate through each of the word tuples
    for word_tuple in similar_keys:
        # Get the stemmed version of the word type
        normalized = stemmer.stem(word_tuple[0])

        # Create a set of postings to add. It will contain 1 copy of all postings from each of the instances of this
        # word type
        new_postings = set()

        # Go through each of the keys associated with this word type
        for word in word_tuple:
            # Add, to the set of new postings, the postings list from the old index for this word
            new_postings.update(index[word])

        # Create a new key for the new index based on the stemmed version of the word type.
        # This key should be associated with the sorted version of the list of new postings
        new_index[normalized] = sorted(list(new_postings))

    # Sort index by keys
    new_index = dict(sorted(new_index.items()))

    print("Saving to file: output/5. stemmed_index.txt")

    with open("output/5. stemmed_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


if __name__ == '__main__':
    main()
