from tkinter import Tk, filedialog


def select_folder():
    root = Tk()
    root.withdraw()           # Hide the small Tkinter window
    root.attributes("-topmost", True)

    folder = filedialog.askdirectory()

    root.destroy()

    return folder