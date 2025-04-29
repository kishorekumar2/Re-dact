import pandas as pd
import re
from tkinter import filedialog

def is_sensitive(text, redaction_types):
    # Define regex patterns for different PII types
    patterns = {
        "name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b",  # Simple name pattern (e.g., "John Doe")
        "address": r"\b\d{1,4}\s[A-Za-z0-9\s.,#-]{5,}\b",  # Basic address pattern
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email pattern
        "phone": r"\b(?:\+?(\d{1,3}))?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})\b",  # Phone pattern
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",  # Credit card pattern
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b"  # Social Security Number pattern
    }
    
    # Check if the text matches any of the specified redaction types
    for redaction_type in redaction_types:
        if re.search(patterns[redaction_type], text):
            return True
    return False

def redact_text(text, redaction_types):
    if is_sensitive(text, redaction_types):
        return "[REDACTED]"
    return text

def process_csv(filepath, redaction_types, progress_callback=None):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)

        # Get the total number of cells for progress calculation
        total_cells = df.size
        processed_cells = 0

        # Redact the sensitive information in the entire DataFrame
        def redact_row(row):
            nonlocal processed_cells
            for column in df.columns:
                row[column] = redact_text(str(row[column]), redaction_types)
                processed_cells += 1
                # Update progress callback every 100 cells processed
                if processed_cells % 100 == 0 and progress_callback:
                    progress_callback((processed_cells / total_cells) * 100)
            return row

        # Apply the redact_row function to each row in the DataFrame
        df = df.apply(redact_row, axis=1)

        # Final progress update
        if progress_callback:
            progress_callback(100)  # Complete

        # Save the redacted file
        redacted_csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if redacted_csv_path:
            df.to_csv(redacted_csv_path, index=False)
            return redacted_csv_path

    except Exception as e:
        raise Exception(f"Error processing CSV: {e}")
