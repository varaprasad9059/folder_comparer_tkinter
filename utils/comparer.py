def get_new_files(old_files, new_files):
    """
    Returns only newly added files.
    """

    return sorted(new_files - old_files)