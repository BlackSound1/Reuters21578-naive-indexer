import json
import sys
from pathlib import Path

from nltk.stem import PorterStemmer


def _search_query(query, file: Path, mode: int) -> list:
    """
    Search the inverted index for the user-given query.

    It is possible for the query to not exist in the inverted index, show a message when this happens.

    :param query: The query to search the inverted index for
    :param file: The file to read the index of
    :param mode: Whether this is to be run on the compressed or uncompressed index
    :return: A possible list of docIDs, if any were found
    """

    # Read the inverted index
    inverted_index = _read_file(file)

    # Look through all keys, to find all that contain the query
    postings = []
    for key in inverted_index.keys():
        if query in key:
            postings.extend(inverted_index[key])

    print(f"\nThe list of articles the query \"{query}\" is found in: "
          f"{inverted_index[query] if postings else []}")

    # Return all postings found, if any
    return postings


def _read_file(file: Path) -> dict:
    """
    Try to read the naive_indexer.txt file.

    Print an error message and exit if unable to

    :return: The inverted index as a dictionary, if possible.
    """

    # Try to read the inverted index, if it exists
    try:
        with open(file, 'rt') as f:
            inverted_index: dict = json.load(f)
        return inverted_index

    # If it doesn't, exit immediately
    except FileNotFoundError:
        sys.exit(f"\nThe required file ({str(file)}), does not exist.")


def query_processor(index: Path, subproject: int = 1) -> None:
    """
    Validate three sample queries.

    Search the given files inverted index for the terms and print results to a file

    :param index: The file Path to read the index of and search the queries in
    :param subproject: Whether this is to be run on the compressed or uncompressed index
    """

    # Create 3 sample queries for testing
    SAMPLE_QUERY_1 = "abnormally"  # This tests stemming
    SAMPLE_QUERY_2 = "017"  # This tests number-removal
    SAMPLE_QUERY_3 = "Zweig"  # This tests case-folding

    # Create Porter stemmer for normalizing search queries
    stemmer = PorterStemmer()

    # Create 3 sample queries for searching. Make sure they are normalized before
    # searching so both indexes have the terms
    SAMPLE_QUERY_4 = stemmer.stem("males".lower())
    SAMPLE_QUERY_5 = stemmer.stem("CORRECTED".lower())
    SAMPLE_QUERY_6 = stemmer.stem("texts".lower())

    # Search the required index for those test queries
    print("\nRunning test queries...")
    RESULT_1 = _search_query(SAMPLE_QUERY_1, index, subproject)
    RESULT_2 = _search_query(SAMPLE_QUERY_2, index, subproject)
    RESULT_3 = _search_query(SAMPLE_QUERY_3, index, subproject)

    # Search the required index for those search queries
    print("\nRunning search queries...")
    RESULT_4 = _search_query(SAMPLE_QUERY_4, index, subproject)
    RESULT_5 = _search_query(SAMPLE_QUERY_5, index, subproject)
    RESULT_6 = _search_query(SAMPLE_QUERY_6, index, subproject)

    # Create dicts to save to file
    RESULT_DICT_TEST = {SAMPLE_QUERY_1: RESULT_1, SAMPLE_QUERY_2: RESULT_2, SAMPLE_QUERY_3: RESULT_3}
    RESULT_DICT_SEARCH = {SAMPLE_QUERY_4: RESULT_4, SAMPLE_QUERY_5: RESULT_5, SAMPLE_QUERY_6: RESULT_6}

    print("\nSaving results to file...")

    # Decide whether to save to a file for the compressed or uncompressed
    file_name = ""
    if subproject == 1:
        file_name = "uncompressed_index.txt"
    elif subproject == 3:
        file_name = "compressed_index.txt"

    TEST_DIR = "query_results/test_queries"
    SEARCH_DIR = "query_results/search_queries"

    # Make sure necessary paths exist
    Path(TEST_DIR).mkdir(parents=True, exist_ok=True)
    Path(SEARCH_DIR).mkdir(parents=True, exist_ok=True)

    # Save to test_queries directory
    print(f'\nSaving test query results to file: {TEST_DIR}/{file_name}')
    with open(f"query_results/test_queries/{file_name}", 'wt') as f:
        json.dump(RESULT_DICT_TEST, f, indent=4)

    # Save to search_queries directory
    print(f'\nSaving search query results to file: {SEARCH_DIR}/{file_name}')
    with open(f"query_results/search_queries/{file_name}", 'wt') as f:
        json.dump(RESULT_DICT_SEARCH, f, indent=4)
