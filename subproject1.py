from glob import glob
from pathlib import Path
from re import sub
from typing import List, Tuple, Dict
from collections import defaultdict
import json

from bs4 import BeautifulSoup
from bs4.element import Tag
from nltk import word_tokenize


def main():
    # Get all reuters objects in the corpus
    ALL_TEXTS: List[Tag] = get_texts()

    # Create a list of (term, docID) pairs
    F: List[Tuple] = []

    # Go through each text in the corpus and create (term, docID) pairs, and add them to the existing list
    for i, text in enumerate(ALL_TEXTS):
        # Find the docID for this document
        DOC_ID = int(text.attrs['newid'])

        # Create list of tokens
        tokens = tokenize(text)

        # Create (term, docID) pairs from those tokens, and add to existing list
        F.extend(create_pairs(tokens, DOC_ID))

    # Sort the list of tuples by term
    F = sorted(F)

    # Create an index for the list of (term, docID) pairs
    index = create_index(F)

    # Save results to file
    save_to_file(index)


def save_to_file(index: dict) -> None:
    with open("output/naiive_indexer.txt", "wt") as f:
        json.dump(index, f)


def create_index(pairs: List[Tuple[str, int]]) -> Dict[str, list]:
    index = defaultdict(list)

    for tup in pairs:
        this_term = tup[0]
        this_doc_id = tup[1]

        index[this_term] += [this_doc_id]

    return dict(index)


def create_pairs(tokens: List[str], docID: int) -> list:
    pairs: List[Tuple[str, int]] = [(token, docID) for token in tokens]

    return pairs


def tokenize(document: Tag) -> list:
    # Text is given as an individual document. Get the only document text in the list of 'text' tags in the document
    doc_text = document('text')[0]

    # Get the text of the article without the 'dateline' or 'title' tag, as this adds clutter
    this_text = '\n'.join(tag.text for tag in doc_text.children if tag.name not in ['dateline', 'title'])

    # Clean the text, so that I can tokenize more properly
    cleaned_text = clean(this_text)

    # Tokenize the text
    tokenized: List[str] = word_tokenize(cleaned_text)

    # Lower-case the text, keeping acronyms capitalized
    lower_cased: List[str] = [token.lower() if not token.isupper() else token for token in tokenized]

    # Remove duplicates
    no_dupes = set(lower_cased)

    # Sort alphabetically
    sort = sorted(no_dupes)

    return sort


def get_texts() -> List[Tag]:
    # Get a list of all corpus files to read
    CORPUS_FILES: List[Path] = [Path(p) for p in glob("../reuters21578/*.sgm")]
    print("\nFound files:\n", [f"{f}" for f in CORPUS_FILES])

    # Create a list, to be populated later, of actual articles in this corpus
    all_articles: List[Tag] = []

    # Loop though each file in the corpus
    for file in CORPUS_FILES:

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
    # Make sure all newline characters have a space after to prevent future tokenization errors, as found in experiment
    text = text.replace('\n', '\n ')

    # Remove all instances of multiple - in a row
    text = sub(r'-{2,}', ' ', text)

    # Remove - characters without letters surrounding them. i.e. Keeps "once-in-a-lifetime", but not " - "
    text = sub(r'(?![A-Za-z])-(?![A-Za-z])', ' ', text)

    # Remove certain unicode control characters, as found in experiment
    text = sub(r'\x03|\x02|\x07|\x05|\xfc|\u007F', '', text)

    # Remove all numbers
    text = sub(r'\d', '', text)

    # Simplify acronyms to their constituent letters. i.e. changes "U.S." to "US"
    text = sub(r"(?<!\w)([A-Za-z])\.", r'\1', text)

    # Remove all punctuation and special characters
    text = sub(r"[()<>{}!$=@&*-/+.,:;?\"]+", ' ', text)

    # Remove all instances of multiple periods in a row
    text = sub(r"\.{2,}", ' ', text)

    # Remove all apostrophes surrounded by letters. In other words, replace all "it's" with "its", etc.
    text = sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", '', text)

    # Remove all apostrophes remaining. Needed to do this separately, because we needed to replace contraction
    # apostrophes with the blank string. We will replace all other apostrophes with a space
    text = sub(r"'", ' ', text)

    return text


if __name__ == '__main__':
    main()
