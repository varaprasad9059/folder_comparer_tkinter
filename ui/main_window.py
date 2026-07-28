import customtkinter as ctk
from utils.folder_picker import select_folder
from utils.scanner import scan_folder
from utils.comparer import get_new_files
from tkinter import ttk
import pandas as pd
from tkinter import filedialog, messagebox
import os



class FolderComparerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ---------------- Window ----------------

        self.title("Folder Difference Finder")

        self.geometry("1100x700")

        self.minsize(1000, 650)

        ctk.set_appearance_mode("System")

        ctk.set_default_color_theme("blue")


        # ---------------- Variables ----------------

        self.old_folder = ""

        self.new_folder = ""

        # ---------------- Build UI ----------------

        self.create_widgets()

    def create_widgets(self):

        ####################################################
        # Title
        ####################################################

        title = ctk.CTkLabel(
            self,
            text="Folder Difference Finder",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=20)

        ####################################################
        # Main Frame
        ####################################################

        self.main_frame = ctk.CTkFrame(self)

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ####################################################
        # OLD Folder
        ####################################################

        old_label = ctk.CTkLabel(
            self.main_frame,
            text="Old Folder"
        )

        old_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.old_entry = ctk.CTkEntry(
            self.main_frame,
            width=800
        )

        self.old_entry.pack(
            side="top",
            padx=20,
            fill="x"
        )

        self.old_button = ctk.CTkButton(
            self.main_frame,
            text="Browse",
            command=self.select_old_folder
        )

        self.old_button.pack(
            padx=20,
            pady=10,
            anchor="e"
        )

        ####################################################
        # NEW Folder
        ####################################################

        new_label = ctk.CTkLabel(
            self.main_frame,
            text="New Folder"
        )

        new_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.new_entry = ctk.CTkEntry(
            self.main_frame,
            width=800
        )

        self.new_entry.pack(
            padx=20,
            fill="x"
        )

        self.new_button = ctk.CTkButton(
            self.main_frame,
            text="Browse",
            command=self.select_new_folder
        )

        self.new_button.pack(
            padx=20,
            pady=10,
            anchor="e"
        )

        ####################################################
        # Compare Button
        ####################################################

        self.compare_button = ctk.CTkButton(
            self.main_frame,
            text="Compare Folders",
            height=45,
            command=self.compare_folders
        )

        self.compare_button.pack(
            pady=25
        )

        ####################################################
        # Stats
        ####################################################

        self.stats = ctk.CTkLabel(
            self.main_frame,
            text="Old Files : 0      New Files : 0      Added : 0",
            font=("Segoe UI", 15)
        )

        self.stats.pack()

        ####################################################
        # Results Placeholder
        ####################################################

        self.result_frame = ctk.CTkFrame(
            self.main_frame,
            height=350
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        # ==========================
        # Treeview
        # ==========================

        columns = ("File Name", "Extension", "Relative Path")

        self.tree = ttk.Treeview(
            self.result_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("File Name", text="File Name")
        self.tree.heading("Extension", text="Extension")
        self.tree.heading("Relative Path", text="Relative Path")

        self.tree.column("File Name", width=250)
        self.tree.column("Extension", width=100)
        self.tree.column("Relative Path", width=700)

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(
            self.result_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")


        self.export_button = ctk.CTkButton(
        self.main_frame,
        text="Export to Excel",
        command=self.export_to_excel
    )

        self.export_button.pack(pady=10)

    

    def select_old_folder(self):

        folder = select_folder()

        if folder:
            self.old_folder = folder

            self.old_entry.delete(0, "end")

            self.old_entry.insert(0, folder)


    def select_new_folder(self):

        folder = select_folder()

        if folder:
            self.new_folder = folder

            self.new_entry.delete(0, "end")

            self.new_entry.insert(0, folder)



    def compare_folders(self):

        if not self.old_folder or not self.new_folder:
            print("Please select both folders.")
            return

        # Scan folders
        old_files = scan_folder(self.old_folder)
        new_files = scan_folder(self.new_folder)

        # Compare
        added_files = get_new_files(old_files, new_files)

        self.added_files = added_files

        # Clear previous rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        import os

        # Insert new rows
        for file in added_files:

            filename = os.path.basename(file)

            extension = os.path.splitext(file)[1]

            self.tree.insert(
                "",
                "end",
                values=(
                    filename,
                    extension,
                    file
                )
            )

        # Update statistics
        self.stats.configure(
            text=f"Old Files : {len(old_files)}      "
                f"New Files : {len(new_files)}      "
                f"Added : {len(added_files)}"
        )

    def export_to_excel(self):

        if not hasattr(self, "added_files") or len(self.added_files) == 0:
            messagebox.showinfo("No Data", "There are no new files to export.")
            return

        data = []

        for file in self.added_files:
            data.append({
                "File Name": os.path.basename(file),
                "Extension": os.path.splitext(file)[1],
                "Relative Path": file
            })

        df = pd.DataFrame(data)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel File", "*.xlsx")],
            initialfile="New_Files_Report.xlsx"
        )

        if file_path:
            df.to_excel(file_path, index=False)

            messagebox.showinfo(
                "Success",
                f"Excel file saved successfully.\n\n{file_path}"
            )