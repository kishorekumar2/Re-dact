import os
from tkinter import filedialog, Tk, Label, Button, messagebox, Checkbutton, IntVar,StringVar, CENTER
from tkinter.ttk import Progressbar  # Correctly import Progressbar from ttk

# Import processing functions
from redact_csv import process_csv
from redact_pdf import process_pdf
from redact_image import process_image

class RedactionTool:
    def __init__(self, master):
        self.master = master
        master.title("RE-DACT Redaction Tool")
        master.geometry("600x500")

        # Center UI elements
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        # UI Elements
        self.label = Label(master, text="Select a file (CSV, PDF, Image) to anonymize", font=("Arial", 14), anchor=CENTER)
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.upload_button = Button(master, text="Upload File", command=self.upload_file, font=("Arial", 12), width=15)
        self.upload_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.filename_label = Label(master, text="", font=("Arial", 10), fg="blue")
        self.filename_label.grid(row=2, column=0, columnspan=2, pady=5)

        # PII Redaction Types
        self.redaction_types = {
            "name": IntVar(),
            "address": IntVar(),
            "email": IntVar(),
            "phone": IntVar(),
            "ssn": IntVar(),
            "credit_card": IntVar(),
        }

        self.redaction_label = Label(master, text="Select PII Types to Redact:", font=("Arial", 12))
        self.redaction_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Redaction Type Check Buttons
        for i, (text, var) in enumerate(self.redaction_types.items()):
            Checkbutton(master, text=text.capitalize(), variable=var, font=("Arial", 10)).grid(row=4 + i // 2, column=i % 2)

        self.process_button = Button(master, text="Process File", command=self.process_file, state="disabled", font=("Arial", 12), width=15)
        self.process_button.grid(row=10, column=0, columnspan=2, pady=10)

        self.download_button = Button(master, text="Download Processed File", command=self.download_file, state="disabled", font=("Arial", 12), width=20)
        self.download_button.grid(row=11, column=0, columnspan=2, pady=10)

        self.progress_var = StringVar()
        self.progress_var.set("")

        self.progress_label = Label(master, textvariable=self.progress_var, font=("Arial", 10), fg="green")
        self.progress_label.grid(row=12, column=0, columnspan=2, pady=10)

        # Progress bar for large file processing
        self.progress_bar = Progressbar(master, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(row=13, column=0, columnspan=2, pady=5)

        self.filepath = None
        self.file_type = None
        self.processed_content = None

    def upload_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("All files", "*.csv *.pdf *.png *.jpg")])
        if self.filepath:
            file_extension = os.path.splitext(self.filepath)[1].lower()
            if file_extension in ['.csv', '.pdf', '.png', '.jpg', '.jpeg']:
                self.filename_label.config(text=f"File selected: {os.path.basename(self.filepath)}")
                self.file_type = file_extension
                self.process_button.config(state="normal")
            else:
                messagebox.showerror("Error", "Unsupported file type!")
        else:
            messagebox.showerror("Error", "No file selected!")

    def process_file(self):
        if self.filepath:
            try:
                # Reset progress bar and message
                self.progress_bar['value'] = 0
                self.progress_var.set("Processing...")
                self.progress_bar.start()

                # Collect selected redaction types
                selected_types = [key for key, var in self.redaction_types.items() if var.get() == 1]

                if not selected_types:
                    messagebox.showerror("Error", "Please select at least one PII type to redact!")
                    return

                if self.file_type == ".csv":
                    self.processed_content = process_csv(self.filepath, selected_types, self.update_progress)
                elif self.file_type == ".pdf":
                    self.processed_content = process_pdf(self.filepath, selected_types, self.update_progress)
                elif self.file_type in [".png", ".jpg", ".jpeg"]:
                    self.processed_content = process_image(self.filepath, selected_types, self.update_progress)

                self.progress_var.set("File processed successfully!")
                self.download_button.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                self.progress_bar.stop()  # Ensure the progress bar stops after processing
        else:
            messagebox.showerror("Error", "No file to process!")

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.master.update_idletasks()  # Update the UI

    def download_file(self):
        if self.processed_content:
            messagebox.showinfo("Download Complete", f"Processed file saved at: {self.processed_content}")
        else:
            messagebox.showwarning("Warning", "No processed file available!")

if __name__ == "__main__":
    root = Tk()
    app = RedactionTool(root)
    root.mainloop()
