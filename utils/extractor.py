from pathlib import Path
import tempfile
import zipfile


def extract_zip(uploaded_file):
    """
    Extracts the uploaded ZIP file into a temporary folder.
    Returns:
        root_folder (Path)
        temp_dir (TemporaryDirectory)
    """

    temp_dir = tempfile.TemporaryDirectory()
    extract_path = Path(temp_dir.name)

    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # Handle ZIPs that contain one top-level folder
    items = list(extract_path.iterdir())

    if len(items) == 1 and items[0].is_dir():
        root_folder = items[0]
    else:
        root_folder = extract_path

    return root_folder, temp_dir