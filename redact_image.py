from PIL import Image, ImageDraw
import pytesseract
from tkinter import filedialog
import re 

def is_sensitive(text, redaction_types):
    # Define regex patterns for different PII types
    patterns = {
        "name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b",
        "address": r"\b\d{1,4}\s[A-Za-z0-9\s.,#-]{5,}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?(\d{1,3}))?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
    }
    
    # Check if the text matches any of the specified redaction types
    for redaction_type in redaction_types:
        if re.search(patterns[redaction_type], text):
            return True
    return False

def process_image(filepath, redaction_types,extra_argument=None):
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        # Check for any sensitive information based on the selected redaction types
        if is_sensitive(text, redaction_types):
            draw = ImageDraw.Draw(image)
            draw.rectangle(((0, 0), (image.size)), fill="black")
        
        redacted_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if redacted_image_path:
            image.save(redacted_image_path)
            return redacted_image_path
    except Exception as e:
        raise Exception(f"Error processing Image: {e}")
