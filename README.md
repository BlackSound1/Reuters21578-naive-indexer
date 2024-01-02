# Reuters21578 Naive Indexer

## Installation
Install the Reuters21578 corpus from http://www.daviddlewis.com/resources/testcollections/reuters21578/. Unzip it and save the folder to the same level as this project. Name the folder `reuters21578`.

Install all dependencies in `requirements.txt`.

## Running
This project is split into three subprojects. Run them with `$ python main.py`.

### Subproject 1
Creates a naive index out of the text of the Reuters21578 corpus.

### Subproject 3
Reads the index created in subproject 1 and performs lossy compression techniques on its dictionary. Shows a table comparing the sizes of the indexes dictionary before and after various compression steps.

### Subproject 2
Queries the index with several single-term queries.
