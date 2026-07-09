from pypdf import PdfReader

def read_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    except Exception as e:
        print(f"Error reading PDF at {file_path}: {e}")
        return ""
    
    return text.strip()