from tkinter import Tk
from tkinter import filedialog


def select_folder(title="Select Folder"):
    """
    Opens a Windows folder selection dialog.

    Returns
    -------
    str
        Selected folder path.
        Returns an empty string if cancelled.
    """

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folder = filedialog.askdirectory(title=title)

    root.destroy()

    return folder