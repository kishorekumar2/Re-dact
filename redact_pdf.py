from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import pytesseract
import re
from tkinter import filedialog

# Specify the path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def is_sensitive(word, redaction_types):
    # Define regex patterns for different PII types
    patterns = {
        "name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b",
        "address": r"\b\d{1,4}\s[A-Za-z0-9\s.,#-]{5,}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?(\d{1,3}))?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
    }
    
    # Check if the word matches any of the specified redaction types
    for redaction_type in redaction_types:
        if re.search(patterns[redaction_type], word):
            return True
    return False

def process_pdf(filepath, redaction_types, extra_argument=None):
    try:
        # Convert PDF to images
        images = convert_from_path(filepath)
        redacted_images = []

        for image in images:
            # Extract text along with bounding box positions
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            draw = ImageDraw.Draw(image)

            # Iterate through all detected words
            for i, word in enumerate(data['text']):
                if is_sensitive(word, redaction_types):
                    # Get bounding box coordinates
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    
                    # Redact the word by drawing a black rectangle over it
                    draw.rectangle([x, y, x + w, y + h], fill="black")
            
            # Add redacted image to the list
            redacted_images.append(image)

        # Save redacted PDF
        redacted_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if redacted_pdf_path:
            redacted_images[0].save(redacted_pdf_path, save_all=True, append_images=redacted_images[1:])
            return redacted_pdf_path
    except Exception as e:
        raise Exception(f"Error processing PDF: {e}")
