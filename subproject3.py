import json
from collections import defaultdict

from nltk.stem import PorterStemmer

from utilities import (calc_postings_size, calc_dict_size, calc_percent_change, render_table)


def subproject_3():
    """
    Read the index generated from `subproject1.py`, and perform various lossy compressions to it, saving
    to additional output files and recording size data along the way. Display a table at the end. Finally,
    run the query processor on the selected three queries again to see what has changed.
    """

    # Read the naive index into memory
    with open('output/1. naive_index.txt', 'rt') as f:
        index = json.load(f)

    # Calculate initial sizes
    INITIAL_DICT_SIZE = calc_dict_size(index)
    INITIAL_POSTINGS_SIZE = calc_postings_size(index)

    # Remove numbers
    print("\nRemoving numbers from the index")
    index = remove_numbers(index)

    # Calculate size data after removing numbers
    NO_NUMS_DICT_SIZE = calc_dict_size(index)
    NO_NUMS_POSTINGS_SIZE = calc_postings_size(index)
    PCT_CHANGE_DICT_SIZE_NO_NUMS = calc_percent_change(NO_NUMS_DICT_SIZE, INITIAL_DICT_SIZE)
    PCT_CHANGE_POSTINGS_SIZE_NO_NUMS = calc_percent_change(NO_NUMS_POSTINGS_SIZE, INITIAL_POSTINGS_SIZE)

    # Do case folding
    print("\nCase-folding the index")
    index = case_folding(index)

    # Calculate size data after case-folding
    CASE_FOLDING_DICT_SIZE = calc_dict_size(index)
    CASE_FOLDING_POSTINGS_SIZE = calc_postings_size(index)
    PCT_CHANGE_DICT_SIZE_CASE_FOLDING = calc_percent_change(CASE_FOLDING_DICT_SIZE, NO_NUMS_DICT_SIZE)
    CML_CHANGE_DICT_SIZE_CASE_FOLDING = calc_percent_change(CASE_FOLDING_DICT_SIZE, INITIAL_DICT_SIZE)
    PCT_CHANGE_POSTINGS_SIZE_CASE_FOLDING = calc_percent_change(CASE_FOLDING_POSTINGS_SIZE, NO_NUMS_POSTINGS_SIZE)
    CML_CHANGE_POSTINGS_SIZE_CASE_FOLDING = calc_percent_change(CASE_FOLDING_POSTINGS_SIZE, INITIAL_POSTINGS_SIZE)

    # Find most common stopwords, after case-folding and number removal
    print("\nCreating stopwords list based on the 150 most common terms in the index")
    create_stopwords(index)

    # Remove 30 stopwords
    print("\nRemoving the most common 30 stopwords from the index")
    index30 = stopwords30(index)

    # Calculate size data after removing 30 stopwords
    STOPW30_DICT_SIZE = calc_dict_size(index30)
    STOPW30_POSTINGS_SIZE = calc_postings_size(index30)
    PCT_CHANGE_DICT_SIZE_30_STOPW = calc_percent_change(STOPW30_DICT_SIZE, CASE_FOLDING_DICT_SIZE)
    CML_CHANGE_DICT_SIZE_30_STOPW = calc_percent_change(STOPW30_DICT_SIZE, INITIAL_DICT_SIZE)
    PCT_CHANGE_POSTINGS_SIZE_30_STOPW = calc_percent_change(STOPW30_POSTINGS_SIZE, CASE_FOLDING_POSTINGS_SIZE)
    CML_CHANGE_POSTINGS_SIZE_30_STOPW = calc_percent_change(STOPW30_POSTINGS_SIZE, INITIAL_POSTINGS_SIZE)

    # Remove 150 stopwords
    print("\nRemoving the most common 150 stopwords from the index")
    index150 = stopwords150(index)

    # Calculate size data after removing 150 stopwords
    STOPW150_DICT_SIZE = calc_dict_size(index150)
    STOPW150_POSTINGS_SIZE = calc_postings_size(index150)
    PCT_CHANGE_DICT_SIZE_150_STOPW = calc_percent_change(STOPW150_DICT_SIZE, CASE_FOLDING_DICT_SIZE)
    CML_CHANGE_DICT_SIZE_150_STOPW = calc_percent_change(STOPW150_DICT_SIZE, INITIAL_DICT_SIZE)
    PCT_CHANGE_POSTINGS_SIZE_150_STOPW = calc_percent_change(STOPW150_POSTINGS_SIZE, CASE_FOLDING_POSTINGS_SIZE)
    CML_CHANGE_POSTINGS_SIZE_150_STOPW = calc_percent_change(STOPW150_POSTINGS_SIZE, INITIAL_POSTINGS_SIZE)

    # Stem
    print("\nStemming the index")
    index = stem(index150)

    # Calculate size data after stemming
    STEM_DICT_SIZE = calc_dict_size(index)
    STEM_POSTINGS_SIZE = calc_postings_size(index)
    PCT_CHANGE_DICT_SIZE_STEM = calc_percent_change(STEM_DICT_SIZE, STOPW150_DICT_SIZE)
    CML_CHANGE_DICT_SIZE_STEM = calc_percent_change(STEM_DICT_SIZE, INITIAL_DICT_SIZE)
    PCT_CHANGE_POSTINGS_SIZE_STEM = calc_percent_change(STEM_POSTINGS_SIZE, STOPW150_POSTINGS_SIZE)
    CML_CHANGE_POSTINGS_SIZE_STEM = calc_percent_change(STEM_POSTINGS_SIZE, INITIAL_POSTINGS_SIZE)

    # Render the table to the console, featuring all the computed data
    render_table(CASE_FOLDING_DICT_SIZE, CASE_FOLDING_POSTINGS_SIZE, CML_CHANGE_DICT_SIZE_150_STOPW,
                 CML_CHANGE_DICT_SIZE_30_STOPW, CML_CHANGE_DICT_SIZE_CASE_FOLDING, CML_CHANGE_DICT_SIZE_STEM,
                 CML_CHANGE_POSTINGS_SIZE_150_STOPW, CML_CHANGE_POSTINGS_SIZE_30_STOPW,
                 CML_CHANGE_POSTINGS_SIZE_CASE_FOLDING, CML_CHANGE_POSTINGS_SIZE_STEM, INITIAL_DICT_SIZE,
                 INITIAL_POSTINGS_SIZE, NO_NUMS_DICT_SIZE, NO_NUMS_POSTINGS_SIZE, PCT_CHANGE_DICT_SIZE_150_STOPW,
                 PCT_CHANGE_DICT_SIZE_30_STOPW, PCT_CHANGE_DICT_SIZE_CASE_FOLDING, PCT_CHANGE_DICT_SIZE_NO_NUMS,
                 PCT_CHANGE_DICT_SIZE_STEM, PCT_CHANGE_POSTINGS_SIZE_150_STOPW, PCT_CHANGE_POSTINGS_SIZE_30_STOPW,
                 PCT_CHANGE_POSTINGS_SIZE_CASE_FOLDING, PCT_CHANGE_POSTINGS_SIZE_NO_NUMS, PCT_CHANGE_POSTINGS_SIZE_STEM,
                 STEM_DICT_SIZE, STEM_POSTINGS_SIZE, STOPW150_DICT_SIZE, STOPW150_POSTINGS_SIZE, STOPW30_DICT_SIZE,
                 STOPW30_POSTINGS_SIZE)


def remove_numbers(index: dict) -> dict:
    """
    Remove all numeric keys in the given index.

    Create a new index, keeping only the items from the given index that are non-numeric, discarding postings lists
    as necessary

    :param index: The index to remove items with numeric keys from
    :return: A new index, based on the given index, without numeric keys
    """

    # Create a new index based on the given index, keeping only non-numeric keys
    new_index = {key: val for key, val in index.items() if not key.isnumeric()}

    print("Saving to file: output/2. no_numbers_index.txt")

    with open("output/2. no_numbers_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def case_folding(index: dict) -> dict:
    """
    Handle case-folding the keys of the given index.

    If 2 or more original keys case-fold to the same new key, must append their postings lists together,
    keeping only unique postings, and sorting the resulting list.

    The result should, itself, be sorted by key, alphabetically.

    Creates a new index based on the given index to avoid errors.

    :param index: The index to case-fold keys for
    :return: A new index, based on the given index, that has case-folded versions of the given indexes keys.
             Should be smaller than the given index. Should not lose any postings. Should have unique
             and sorted postings for each key.
    """

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
    """
    Create a new index, based on the given index, with 30 stopword keys removed.

    Eliminates the keys corresponding to stopwords completely, not preserving their postings lists.

    Creates a new index based on the given index to avoid errors.

    :param index: The index to remove 30 stopword keys for
    :return: A new index, based on the given index, with all keys corresponding to 30 stopwords removed.
    """

    # Get the first 30 stopwords from stopwords.txt. The file has the 150 most common words in the corpus
    with open('stopwords.txt', 'rt') as f:
        STOPWORDS = [word.strip() for word in f.readlines()][:30]

    # Create new index based on whether the keys of the old index are stopwords
    new_index = {key: val for key, val in index.items() if key not in STOPWORDS}

    print("Saving to file: output/4a. 30_stopwords_index.txt")

    with open("output/4a. 30_stopwords_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def stopwords150(index: dict) -> dict:
    """
    Create a new index, based on the given index, with 150 stopword keys removed.

    Eliminates the keys corresponding to stopwords completely, not preserving their postings lists.

    Creates a new index based on the given index to avoid errors.

    :param index: The index to remove 150 stopword keys for
    :return: A new index, based on the given index, with all keys corresponding to 150 stopwords removed.
    """

    # Get all stopwords from stopwords.txt. The file has the 150 most common words in the corpus
    with open('stopwords.txt', 'rt') as f:
        STOPWORDS = [word.strip() for word in f.readlines()]

    # Create new index based on whether the keys of the old index are stopwords
    new_index = {key: val for key, val in index.items() if key not in STOPWORDS}

    print("Saving to file: output/4b. 150_stopwords_index.txt")

    with open("output/4b. 150_stopwords_index.txt", "wt") as f:
        json.dump(new_index, f)

    return new_index


def stem(index: dict) -> dict:
    """
    Handle stemming the keys of the given index.

    If 2 or more original keys stem to the same new key, must append their postings lists together,
    keeping only unique postings, and sorting the resulting list.

    The result should, itself, be sorted by key, alphabetically.

    Creates a new index based on the given index to avoid errors.

    :param index: The index to stem keys for
    :return: A new index, based on the given index, that has stemmed versions of the given indexes keys.
             Should be smaller than the given index. Should not lose any postings. Should have unique
             and sorted postings for each key.
    """

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


def create_stopwords(index: dict) -> None:
    """
    Create a list of the 150 most common terms in the index.

    This needs to be done here, so that the terms are as normalized as possible before we need the stopwords
    for their removal. It would be bad if 'the' and 'The' were different stopwords, for instance, so it's best to
    do this after case-folding. Needs to happen before stemming though, as per the table I'm trying to emulate.

    Finds the most common terms by seeing which terms have the longest postings list.

    :param index: The index to find the most common terms of
    """

    # Sort by most common dictionary terms. Inspired by https://stackoverflow.com/a/50863131
    sorted_index = dict(sorted(index.items(), key=lambda x: len(x[1]), reverse=True))

    # Get only the 150 most common tokens
    most_common_tokens_150 = list(sorted_index.keys())[:150]

    # Save them to a file
    print("Saving to file: stopwords.txt")
    with open('stopwords.txt', 'wt') as f:
        f.write('\n'.join(token for token in most_common_tokens_150))
