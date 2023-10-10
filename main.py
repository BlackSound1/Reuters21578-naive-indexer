from pathlib import Path

import subproject1
import subproject2
import subproject3


if __name__ == '__main__':
    """Run the whole project"""

    # Run subproject 1
    print("\nRUNNING SUBPROJECT 1...")
    subproject1.subproject_1()

    # Run subproject 3
    print("\n-----------------\n\nRUNNING SUBPROJECT 3...")
    subproject3.subproject_3()

    # Run the subproject 2 query processor on the uncompressed naive index
    print("\n-----------------\n\nRUNNING SUBPROJECT 2 (on uncompressed index)")
    subproject2.sample_query_processor(Path('output/1. naive_index.txt'), subproject=1)

    # Run the subproject 2 query processor on the compressed naive index
    print("\n-----------------\n\nRUNNING SUBPROJECT 2 (on compressed index)")
    subproject2.sample_query_processor(Path('output/5. stemmed_index.txt'), subproject=3)

    # Run the subproject 2 query processor on challenge queries
    print("\n-----------------\n\nRUNNING SUBPROJECT 2 (on challenge queries)")
    subproject2.challenge_query_processor(['interesting', 'progress', 'powerful'])
