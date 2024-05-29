import glob
import os
from pathlib import Path

import pandas as pd
from invoke import task
from tabulate import tabulate


@task
def camelot_file(
    ctx,
    pdf_fpath: str,
    mode: str = "lattice",
    first_page: int = 1,
    last_page: str = "end",
    display: bool = False,
) -> None:
    """Exracts all tables from the specified PDF pages Camelot."""

    if mode not in {"stream", "lattice"}:
        print("💥 'mode' must be one of 'lattice' OR 'stream'")
        return

    extraction_dir = "./extractions"
    os.makedirs(extraction_dir, exist_ok=True)

    pdf_path = Path(pdf_fpath)
    fname = pdf_path.name.replace(".pdf", "")
    out_path = os.path.join(extraction_dir, f"{fname}.csv")

    # Extract using Camelot
    ctx.run(
        "camelot -f csv "
        f"-p {first_page}-{last_page} "
        f"-o {out_path} {mode} {pdf_path}"
    )
    if display:
        # # Gather all the csv files and display
        # df = pd.concat(
        #     [
        #         pd.read_csv(
        #             tab,
        #             header=None,
        #         )
        #         for tab in glob.glob(f"{extraction_dir}/{fname}-page-*-table-*.csv")
        #     ],
        #     axis=1,
        #     ignore_index=True,
        # ).dropna(thresh=1)

        # print(tabulate(df))

        tables_found = glob.glob(f"{extraction_dir}/{fname}-page-*-table-*.csv")
        for tab in tables_found:
            print(
                tabulate(pd.read_csv(tab, header=None).dropna(thresh=1), headers="keys")
            )
