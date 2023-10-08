import json
import sys
from pathlib import Path


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

    # If query not found, print a message and return empty list
    if query not in inverted_index.keys():
        if mode == 1:
            print(f"\nThe query of {query} does not exist in the uncompressed inverted index")

        elif mode == 3:
            print(f"\nThe query of {query} does not exist in the compressed inverted index")

        return []

    # If query found, print the list and return it
    else:
        print(f"\nThe list of articles the query \"{query}\" is found in:")
        print(f"\n{inverted_index[query]}")

        return inverted_index[query]


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


def query_processor(file: Path, mode: int = 1) -> None:
    """
    Validate three sample queries.

    Search the given files inverted index for the terms and print results to a file

    :param file: The file to read the index of and search the queries in
    :param mode: Whether this is to be run on the compressed or uncompressed index
    """

    # Create 3 sample queries
    SAMPLE_QUERY_1 = "abnormally"  # This tests stemming
    SAMPLE_QUERY_2 = "017"  # This tests number-removal
    SAMPLE_QUERY_3 = "Zweig"  # This tests case-folding

    # Search the required index for those queries
    RESULT_1 = _search_query(SAMPLE_QUERY_1, file, mode)
    RESULT_2 = _search_query(SAMPLE_QUERY_2, file, mode)
    RESULT_3 = _search_query(SAMPLE_QUERY_3, file, mode)

    # Create dict to save to file
    RESULT_DICT = {SAMPLE_QUERY_1: RESULT_1, SAMPLE_QUERY_2: RESULT_2, SAMPLE_QUERY_3: RESULT_3}

    # Save file, depending on whether this is being run in subproject1 or 3
    if mode == 1:
        print("\nSaving query results to file: query_results/uncompressed.txt")
        with open('query_results/uncompressed.txt', 'wt') as f:
            json.dump(RESULT_DICT, f, indent=4)

    elif mode == 3:
        print("\nSaving query results to file: query_results/compressed.txt")
        with open('query_results/compressed.txt', 'wt') as f:
            json.dump(RESULT_DICT, f, indent=4)
