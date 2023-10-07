from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box


def calc_percent_change(new: float, old: float) -> float:
    return round(((new - old) / old) * 100, 2)


def calc_dict_size(index: dict) -> int:
    return len(index.keys())


def calc_postings_size(index: dict) -> int:
    return sum(len(x) for x in index.values())


def create_main_table():
    main_table = Table(title="Effect of Processing for Reuters21578", box=box.MINIMAL, safe_box=True)
    main_table.add_column("Size of")
    main_table.add_column("Word types (terms)")
    main_table.add_column("Non-positional postings")
    return main_table


def create_word_types_table():
    word_types_table = Table(title="Dictionary", box=box.MINIMAL, expand=True)
    word_types_table.add_column("Size", no_wrap=True)
    word_types_table.add_column("% Change", no_wrap=True)
    word_types_table.add_column("% Change (cml.)", no_wrap=True)
    return word_types_table


def create_postings_table():
    postings_table = Table(title="Non-positional index", box=box.MINIMAL, expand=True, pad_edge=False)
    postings_table.add_column("Size", no_wrap=True, overflow='ignore')
    postings_table.add_column("% Change", no_wrap=True, overflow='ignore')
    postings_table.add_column("% Change (cml.)", no_wrap=True, overflow='ignore')
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
    text_align = Align("\n\n\n\nUnfiltered\nNo numbers\nCase folding\n30 stopw's\n150 stopw's\nStemming",
                       vertical='middle')

    # Add everything to the main table
    main_table.add_row(text_align, word_types_table, postings_table)

    # Render the table to the Console
    console = Console()
    console.print()
    console.print(main_table)
