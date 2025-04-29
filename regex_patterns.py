# regex_patterns.py

# Regex pattern for emails
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# Regex pattern for phone numbers (supports international format as well)
PHONE_PATTERN = r"\b(?:\+?(\d{1,3}))?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})\b"

# Regex pattern for credit card numbers
CREDIT_CARD_PATTERN = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"

# Regex pattern for addresses (generalized)
ADDRESS_PATTERN = r"\b\d{1,4}\s[A-Za-z0-9\s.,#-]{5,}\b"

# Regex pattern for Social Security Numbers (SSNs)
SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"

# Add other PII patterns as needed
