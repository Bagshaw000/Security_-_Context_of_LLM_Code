# Splits one of main.py's aggregate result JSON files (result/<Model><...>.json,
# a single JSON object mapping task index -> generated text) back out into
# individual per-task files on disk: one .py file per task for generated code
# (consumed by src/Complexity_metrics.py and external static analysis tools),
# or one .json file per task for the complexity-ranking responses.
#
# This module is written as a standalone script: the two functions are
# reusable, but the two lines at the bottom actually run when this file is
# executed directly (`python src/write_file.py`) and must be edited by hand
# to point at whichever result file/output folder you want to expand next.
import json

import pandas as pd
from pathlib import Path
from util import clean_json


def create_python_file(file_path:str,model:str):
    """Expand an aggregate JSON result file into one .py file per entry.

    file_path: path to a result/*.json file shaped like {"0": "<code>", "1": "<code>", ...}
    model: name of the output folder to create (e.g. "Claude", "GPTNew") -
           each key becomes "<model>/<key>.py" under the current working directory.

    Uses mode 'x' (exclusive create) so it will raise FileExistsError rather
    than silently overwrite files from a previous run - delete the target
    folder first if you need to regenerate it.
    """
    try:

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Wrapping the dict in a single-row DataFrame is a convenient way to
        # iterate (column_name, value) pairs via df.items() below - it is not
        # otherwise used for tabular analysis here.
        df = pd.DataFrame(data, index=[0])

        for col_name, col_data  in df.items():

            file_name = str(col_name +".py")
            file_ = str(Path.cwd()/model/file_name)

            folder_path = Path(file_)
            folder_path.parent.mkdir(parents=True, exist_ok=True)

            # col_data is a one-element pandas Series; .item() unwraps it to
            # the raw generated-code string.
            with open(file_, 'x',encoding='utf-8') as file:
                file.write(col_data.item())

    except Exception as e:
        raise e


def create_json_file(file_path:str,model:str):
    """Expand an aggregate JSON result file into one cleaned .json file per entry.

    Same shape/behavior as create_python_file(), but for the complexity-ranking
    responses produced by main.py's rank_prompt(): each value is passed through
    util.clean_json() first to strip markdown code-fence artifacts (```json, ```)
    that models sometimes wrap their JSON answers in, before being written out
    as "<model>/<key>.json".
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data, index=[0])

        for col_name, col_data  in df.items():
            clean = clean_json(col_data.item())
            file_name = str(col_name +".json")
            file_ = str(Path.cwd()/model/file_name)

            folder_path = Path(file_)
            folder_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_, 'x',encoding='utf-8') as file:
                file.write(clean)
    except Exception as e:
        raise e


# Script entry point: edit these two lines to point at the result file you
# want to expand and the output folder it should be split into, then run
# `python src/write_file.py` from the project root.
p = Path("result/LlamaRankNew2026-07-01.json").resolve()
create_json_file(p,"LlamaRankNew")
