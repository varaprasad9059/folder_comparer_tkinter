def get_new_files(old_files, new_files):
    """
    Returns only files present in the new folder
    but not in the old folder.
    """

    return sorted(new_files - old_files)