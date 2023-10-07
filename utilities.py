from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box


def calc_percent_change(new: float, old: float) -> float:
    """
    Calculate the percentage change between new and old values.

    Rounds result to 2 decimal places

    :param new: The new value to compare against the old value
    :param old: The old value to act as the base value
    :return: The percentage change between new and old values, rounded to 2 decimal places
    """

    return round(((new - old) / old) * 100, 2)


def calc_dict_size(index: dict) -> int:
    """
    Get how many keys exist in an index

    :param index: The index to find the number of keys in
    :return: The number of keys in the given index
    """

    return len(index.keys())


def calc_postings_size(index: dict) -> int:
    """
    Get the number of total postings in a given index.

    Computes the sum of the lengths of all the postings lists in the index

    :param index: The index to find the total number of postings in
    :return: The number of total postings in the given index
    """

    return sum(len(x) for x in index.values())


def create_main_table():
    """
    Create the main table for showing the effects of lossy compression on the index.

    The table has 3 columns:
     - "Size of" enumerates the different steps of the lossy compression
     - "Word types (terms)" shows the size data for the indexes dictionary, as a sub-table
     - "Non-positional postings" shows the size data of the indexes postings lists, as a sub-table

    :return: The constructed Table object
    """

    main_table = Table(title="Effect of Processing for Reuters-21578", box=box.MINIMAL, safe_box=True)
    main_table.add_column("Size of", justify='center')
    main_table.add_column("Word types (terms)", justify='center')
    main_table.add_column("Non-positional postings", justify='center')
    return main_table


def create_word_types_table():
    """
    Create the sub-table for word type size data.

    The table has 3 columns:
     - "Size" is the numerical size of the indexes dictionary as of the given stage in the lossy compression pipeline
     - "% Change" shows how much this size has changed between this step and the previous step of the pipeline
     - "% Change (cml.)" shows how much this size has changed cumulatively between this step and the initial dictionary

    :return: The constructed Table object
    """

    word_types_table = Table(title="Dictionary", box=box.MINIMAL, expand=True)
    word_types_table.add_column("Size", no_wrap=True, justify='center')
    word_types_table.add_column("% Change", no_wrap=True, justify='center')
    word_types_table.add_column("% Change (cml.)", no_wrap=True, justify='center')
    return word_types_table


def create_postings_table():
    """
    Create the sub-table for postings lists size data.

    The table has 3 columns:
     - "Size" is the total numerical size of the indexes postings lists as of the given stage in the lossy compression pipeline
     - "% Change" shows how much this size has changed between this step and the previous step of the pipeline
     - "% Change (cml.)" shows how much this size has changed cumulatively between this step and the initial indexes postings lists

    :return: The constructed Table object
    """

    postings_table = Table(title="Non-positional index", box=box.MINIMAL, expand=True, pad_edge=False)
    postings_table.add_column("Size", no_wrap=True, overflow='ignore', justify='center')
    postings_table.add_column("% Change", no_wrap=True, overflow='ignore', justify='center')
    postings_table.add_column("% Change (cml.)", no_wrap=True, overflow='ignore', justify='center')
    return postings_table


def render_table(CASE_FOLDING_DICT_SIZE, CASE_FOLDING_POSTINGS_SIZE, CML_CHANGE_DICT_SIZE_150_STOPW,
                 CML_CHANGE_DICT_SIZE_30_STOPW, CML_CHANGE_DICT_SIZE_CASE_FOLDING, CML_CHANGE_DICT_SIZE_STEM,
                 CML_CHANGE_POSTINGS_SIZE_150_STOPW, CML_CHANGE_POSTINGS_SIZE_30_STOPW,
                 CML_CHANGE_POSTINGS_SIZE_CASE_FOLDING, CML_CHANGE_POSTINGS_SIZE_STEM, INITIAL_DICT_SIZE,
                 INITIAL_POSTINGS_SIZE, NO_NUMS_DICT_SIZE, NO_NUMS_POSTINGS_SIZE, PCT_CHANGE_DICT_SIZE_150_STOPW,
                 PCT_CHANGE_DICT_SIZE_30_STOPW, PCT_CHANGE_DICT_SIZE_CASE_FOLDING, PCT_CHANGE_DICT_SIZE_NO_NUMS,
                 PCT_CHANGE_DICT_SIZE_STEM, PCT_CHANGE_POSTINGS_SIZE_150_STOPW, PCT_CHANGE_POSTINGS_SIZE_30_STOPW,
                 PCT_CHANGE_POSTINGS_SIZE_CASE_FOLDING, PCT_CHANGE_POSTINGS_SIZE_NO_NUMS, PCT_CHANGE_POSTINGS_SIZE_STEM,
                 STEM_DICT_SIZE, STEM_POSTINGS_SIZE, STOPW150_DICT_SIZE, STOPW150_POSTINGS_SIZE, STOPW30_DICT_SIZE,
                 STOPW30_POSTINGS_SIZE):
    """
    Render the size data table to the console

    Take in all the computed values for the size data for the dictionary sub-table and the Non-positional
    index sub-table. Create the main table, and it's sub-tables and populate them with this data.

    The number of parameters is too large to enumerate, so I will instead show the pattern in their names.

    - Any parameter ending in "_SIZE" corresponds to a value to be placed in a "Size" column in either the "Dictionary"
      or "Non-positional index" sub-tables. The parameters start with the name of the lossy compression pipeline step it
      refers to.

    - Any parameter with "_DICT_" in its name, will be placed in the "Dictionary" sub-table. Likewise for "_POSTINGS_".

    - Any parameter starting with "PCT_CHANGE" is a non-cumulative percentage change datum. These parameters end with
      what step in the lossy compression pipeline they refer to.

    - Any parameter starting with "CML_CHANGE" is a cumulative percentage change datum. These parameters end with
      what step in the lossy compression pipeline they refer to.
    """

    # Create main table
    main_table = create_main_table()

    # Create word types sub-table
    word_types_table = create_word_types_table()

    # Fill table with data
    word_types_table.add_row(f"{INITIAL_DICT_SIZE:,}", str(0), str(0))
    word_types_table.add_row(f"{NO_NUMS_DICT_SIZE:,}", str(PCT_CHANGE_DICT_SIZE_NO_NUMS),
                             str(PCT_CHANGE_DICT_SIZE_NO_NUMS))
    word_types_table.add_row(f"{CASE_FOLDING_DICT_SIZE:,}", str(PCT_CHANGE_DICT_SIZE_CASE_FOLDING),
                             str(CML_CHANGE_DICT_SIZE_CASE_FOLDING))
    word_types_table.add_row(f"{STOPW30_DICT_SIZE:,}", str(PCT_CHANGE_DICT_SIZE_30_STOPW),
                             str(CML_CHANGE_DICT_SIZE_30_STOPW))
    word_types_table.add_row(f"{STOPW150_DICT_SIZE:,}", str(PCT_CHANGE_DICT_SIZE_150_STOPW),
                             str(CML_CHANGE_DICT_SIZE_150_STOPW))
    word_types_table.add_row(f"{STEM_DICT_SIZE:,}", str(PCT_CHANGE_DICT_SIZE_STEM),
                             str(CML_CHANGE_DICT_SIZE_STEM))

    # Create postings sub-table
    postings_table = create_postings_table()

    # Fill table with data
    postings_table.add_row(f"{INITIAL_POSTINGS_SIZE:,}", str(0), str(0))
    postings_table.add_row(f"{NO_NUMS_POSTINGS_SIZE:,}", str(PCT_CHANGE_POSTINGS_SIZE_NO_NUMS),
                           str(PCT_CHANGE_POSTINGS_SIZE_NO_NUMS))
    postings_table.add_row(f"{CASE_FOLDING_POSTINGS_SIZE:,}", str(PCT_CHANGE_POSTINGS_SIZE_CASE_FOLDING),
                           str(CML_CHANGE_POSTINGS_SIZE_CASE_FOLDING))
    postings_table.add_row(f"{STOPW30_POSTINGS_SIZE:,}", str(PCT_CHANGE_POSTINGS_SIZE_30_STOPW),
                           str(CML_CHANGE_POSTINGS_SIZE_30_STOPW))
    postings_table.add_row(f"{STOPW150_POSTINGS_SIZE:,}", str(PCT_CHANGE_POSTINGS_SIZE_150_STOPW),
                           str(CML_CHANGE_POSTINGS_SIZE_150_STOPW))
    postings_table.add_row(f"{STEM_POSTINGS_SIZE:,}", str(PCT_CHANGE_POSTINGS_SIZE_STEM),
                           str(CML_CHANGE_POSTINGS_SIZE_STEM))

    # Handle first column text
    text_align = Align("\n\n\n\n  Unfiltered\n  No numbers\nCase folding\n  30 stopw's\n 150 stopw's"
                       "\n    Stemming", vertical='middle')

    # Add everything to the main table
    main_table.add_row(text_align, word_types_table, postings_table)

    # Render the table to the Console
    console = Console()
    console.print()
    console.print(main_table)
