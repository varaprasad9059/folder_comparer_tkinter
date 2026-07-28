import pandas as pd
from pathlib import Path


def create_dataframe(file_list):

    rows = []

    for file in file_list:

        p = Path(file)

        rows.append({

            "File Name": p.name,

            "Extension": p.suffix,

            "Folder": str(p.parent),

            "Relative Path": file

        })

    return pd.DataFrame(rows)


def save_excel(df):

    filename = "NewFiles.xlsx"

    df.to_excel(filename, index=False)

    return filename


def save_csv(df):

    filename = "NewFiles.csv"

    df.to_csv(filename, index=False)

    return filename