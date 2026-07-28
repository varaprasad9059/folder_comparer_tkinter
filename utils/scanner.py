from pathlib import Path


def scan_folder(folder_path):
    """
    Scan all files inside a folder recursively.

    Returns
    -------
    set
        Relative file paths.
    """

    folder = Path(folder_path)

    files = set()

    for file in folder.rglob("*"):

        if file.is_file():

            relative = file.relative_to(folder)

            files.add(relative.as_posix())

    return files