import json
from typing import Optional


def main():
    """
    Main functionality for subproject 2.

    Gets user query, makes sure it's a valid query, and checks the inverted index for it.

    Also checks the inverted index for three sample queries.
    """

    # Get user input query
    query = input("\nPlease enter a term to search the inverted index for: ")

    # Strip spaces to the left and right
    query = query.strip()

    # Make sure numeric queries are forbidden
    if query.isnumeric():
        print("\nThe query must be non-numeric. Numbers are not saved to the inverted index")
        return

    # Make sure the query is only a single term
    if ' ' in query:
        print("\nOnly single-term queries are allowed.")
        return

    # Make sure query doesn't contain special characters
    if any(not c.isalpha() for c in query):
        print("\nNo special characters allowed.")
        return

    # Lower-case the query
    query = query.lower()

    # Try to find the users query in the inverted index
    _ = search_query(query)

    print("\n---------------------------")

    # Validate query returns for 2 sample queries
    validate_sample_queries()


def search_query(query) -> Optional[list]:
    """
    Search the inverted index for the user-given query.

    It is possible for the query to not exist in the inverted index, show a message when this happens.

    :param query: The query to search the inverted index for
    :return: A possible list of docIDs, if any were found
    """

    # Try to read the inverted index if it exists
    inverted_index = read_file()
    if not inverted_index:
        return None

    if query not in inverted_index.keys():
        print(f"\nThe query of {query} does not exist in the inverted index")
        return None
    else:
        print(f"\nThe list of articles the query \"{query}\" is found in:")
        print(f"\n{inverted_index[query]}")

        return inverted_index[query]


def read_file() -> Optional[dict]:
    """
    Try to read the naive_indexer.txt file.

    Print and error message if unable to

    :return: The inverted index as a dictionary, if possible.
    """

    try:
        with open('output/naive_indexer.txt', 'rt') as f:
            inverted_index: dict = json.load(f)

        return inverted_index

    except FileNotFoundError:
        print("\nThe required file (output/naive_indexer.txt), does not exist. Please run subproject1.py first")

        return None


def validate_sample_queries() -> None:
    """
    Validate three sample queries.

    Search the inverted index for the terms and make sure the results are as expected
    """

    SAMPLE_QUERY_1 = "abolition"
    EXPECTED_1 = [209, 274, 318, 893, 991, 4670, 4705, 5432, 7051, 8681, 9774, 11122,
                  12241, 12640, 12847, 12887, 12916, 16292, 17703, 18403, 19508, 19543]

    SAMPLE_QUERY_2 = "lifo"
    EXPECTED_2 = [588, 2221, 6084, 6104, 6461, 7061, 8262, 9519, 11320, 11333, 16844, 17808, 18610]

    SAMPLE_QUERY_3 = "zweig"
    EXPECTED_3 = [20518]

    RESULT_1 = search_query(SAMPLE_QUERY_1)
    RESULT_2 = search_query(SAMPLE_QUERY_2)
    RESULT_3 = search_query(SAMPLE_QUERY_3)

    num_valid = 0

    if RESULT_1 == EXPECTED_1:
        num_valid += 1
    else:
        print("\nSomething went wrong with query 1")

    if RESULT_2 == EXPECTED_2:
        num_valid += 1
    else:
        print("\nSomething went wrong with query 2")

    if RESULT_3 == EXPECTED_3:
        num_valid += 1
    else:
        print("\nSomething went wrong with query 3")

    if num_valid == 3:
        print("\nAll 3 queries were valid!")


if __name__ == '__main__':
    main()
