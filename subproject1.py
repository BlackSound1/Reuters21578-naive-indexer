from glob import glob
from pathlib import Path
from re import sub
from typing import List, Tuple, Dict
from collections import defaultdict
import json
import time

from bs4 import BeautifulSoup
from bs4.element import Tag
from nltk import word_tokenize


def main():
    """
    Main function. Runs the whole subproject1 module
    """

    tick = time.time()

    # Get all reuters objects in the corpus
    ALL_TEXTS: List[Tag] = get_texts()

    # Create a list of (term, docID) pairs
    F: List[Tuple] = []

    # Go through each text in the corpus and create (term, docID) pairs, and add them to the existing list
    for text in ALL_TEXTS:
        # Find the docID for this document
        DOC_ID = int(text.attrs['newid'])

        print(f"Creating (term, docID) pairs for article: {DOC_ID}")

        # Create list of tokens
        tokens = process_document(text)

        # Create (term, docID) pairs from those tokens, and add to existing list
        F.extend(create_pairs(tokens, DOC_ID))

    # Sort the list of tuples by term
    F = sorted(F)

    # Create an index for the list of (term, docID) pairs
    print("Creating inverted index")
    index = create_index(F)

    # Save results to file
    print("Saving to file: output/naive_index.txt")
    save_to_file(index)

    tock = time.time()

    print(f"Time taken: {tock - tick}")


def save_to_file(index: dict) -> None:
    """
    Save the computed index to an output file.

    Always saves to `output/naive_indexer.txt`.

    :param index: The index to save to file
    """

    with open("output/naive_index.txt", "wt") as f:
        json.dump(index, f)


def create_index(pairs: List[Tuple[str, int]]) -> Dict[str, list]:
    """
    Create an inverted index based on the list of (term, docID) tuples.

    :param pairs: The list of (term, docID) tuples
    :return: A dictionary of form `{term: [list, of, docIDs]}`
    """

    # Create a defaultdict to allow for saving to dictionary keys that don't yet exist
    index = defaultdict(list)

    # For each (term, docID) pair, get the term and docID and add them to the index
    for tup in pairs:
        this_term = tup[0]
        this_doc_id = tup[1]

        index[this_term] += [this_doc_id]

    return dict(index)


def create_pairs(tokens: List[str], docID: int) -> list:
    """
    Create (term, docID) pairs based on the given list of tokens

    :param tokens: The list of tokens to create (term, docID) pairs with
    :param docID: The docID representing this article
    :return: A list of (term, docID) pairs
    """

    pairs: List[Tuple[str, int]] = [(token, docID) for token in tokens]

    return pairs


def process_document(document: Tag) -> list:
    """
    Perform various textual processing steps on a given document to get ready for future steps.

    :param document: The Reuters document, as represented by a Tag object
    :return: A list of cleaned, tokenized, lower-cased, sorted tokens with no duplicates
    """

    # Text is given as an individual document. Get the only document text in the list of 'text' tags in the document
    doc_text = document('text')[0]

    # Get the text of the article without the 'dateline' or 'title' tag, as this adds clutter
    this_text = '\n'.join(tag.text for tag in doc_text.children if tag.name not in ['dateline', 'title'])

    # Clean the text, so that I can tokenize more properly
    cleaned_text = clean(this_text)

    # Tokenize the text
    tokenized: List[str] = word_tokenize(cleaned_text)

    # Remove duplicates
    no_dupes = set(tokenized)

    return list(no_dupes)


def get_texts() -> List[Tag]:
    """
    Read the Reuters corpus to get all the articles

    :return: A list of Reuters articles, represented by Tag objects
    """

    # Get a list of all corpus files to read
    CORPUS_FILES: List[Path] = [Path(p) for p in glob("../reuters21578/*.sgm")]
    print("\nFound files:\n", [f"{f}" for f in CORPUS_FILES])

    # Create a list, to be populated later, of actual articles in this corpus
    all_articles: List[Tag] = []

    # Loop though each file in the corpus
    for file in CORPUS_FILES:
        print(f"Reading file: {file}")

        # Read the files contents as HTML
        with open(file, 'r') as f:
            contents = BeautifulSoup(f, features='html.parser')

        # Filter this content by 'reuters' tags
        articles = contents('reuters')

        # Add to the all_articles list, the list of articles found in this file. Use .extend to do so in a 'flat' way
        # i.e. Don't want: [1, [2, [3, [4]]]], want: [1, 2, 3, 4]
        all_articles.extend(articles)

    return all_articles


def clean(text: str) -> str:
    """
    Perform mild cleaning of the incoming text to make tokenization easier and more accurate.

    Based on experiment, need to remove Unicode control characters, make sure new lines have a space after,
    simplify acronyms to their constituent letters, remove all punctuation and special characters, remove all
    apostrophes (handle contractions carefully), and remove a srange ^M character.

    :param text: The text to clean
    :return: The cleaned text
    """

    # Make sure all newline characters have a space after to prevent future tokenization errors, as found in experiment
    text = text.replace('\n', '\n ')

    # Remove certain unicode control characters, as found in experiment
    text = sub(r'\x03|\x02|\x07|\x05|\xfc|\u007F', '', text)

    # Simplify acronyms to their constituent letters. i.e. changes "U.S." to "US"
    text = sub(r"(?<!\w)([A-Za-z])\.", r'\1', text)

    # Remove all punctuation and special characters
    text = sub(r"[()<>{}\[\]!$=@&*-/+.,:;?\"]+", ' ', text)

    # Remove "^M" found in experiment
    text = sub(r'\^M', ' ', text)

    # Remove all apostrophes surrounded by letters. In other words, replace all "it's" with "its", etc.
    text = sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '', text)

    # Remove all apostrophes remaining. Needed to do this separately, because we needed to replace contraction
    # apostrophes with the blank string. We will replace all other apostrophes with a space
    text = sub(r"'", ' ', text)

    return text


if __name__ == '__main__':
    main()
