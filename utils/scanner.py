from pathlib import Path


def scan_folder(folder_path):
    """
    Returns a set of relative file paths.
    """

    folder = Path(folder_path)

    files = set()

    for file in folder.rglob("*"):
        if file.is_file():
            files.add(str(file.relative_to(folder)).replace("\\", "/"))

    return files