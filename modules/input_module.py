"""
═══════════════════════════════════════════════════════════════
MODULE 1: INPUT MODULE — File Handling & Text Extraction
═══════════════════════════════════════════════════════════════
Role: Read resume from .txt or .pdf files, or accept raw text.
Tech: Python built-in file handling (open())
═══════════════════════════════════════════════════════════════
"""

import os


def read_text_file(file_path):
    """
    Read a plain text (.txt) resume file.
    
    Args:
        file_path (str): Path to the .txt file
        
    Returns:
        str: Raw text content of the file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    
    if not file_path.lower().endswith('.txt'):
        raise ValueError("Expected a .txt file")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.strip():
        raise ValueError("The resume file is empty")
    
    print(f"  > Successfully read text file: {os.path.basename(file_path)}")
    print(f"  > Characters extracted: {len(content)}")
    return content


def read_pdf_file(file_path):
    """
    Read a PDF resume file using pypdf or fallback extraction.
    
    Args:
        file_path (str): Path to the .pdf file
        
    Returns:
        str: Extracted text content
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError("Expected a .pdf file")
    
    # Try pypdf first
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        extracted_pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_pages.append(text)
        if extracted_pages:
            result = "\n".join(extracted_pages).strip()
            if result:
                print(f"  > Successfully extracted text from PDF with pypdf: {os.path.basename(file_path)}")
                print(f"  > Characters extracted: {len(result)}")
                return result
    except Exception as e:
        print(f"  > pypdf extraction note: {e}")

    # Fallback extraction
    text_parts = []
    with open(file_path, 'rb') as f:
        content = f.read()
    
    try:
        decoded = content.decode('utf-8', errors='ignore')
        in_text = False
        current_text = []
        for i, char in enumerate(decoded):
            if char == '(' and not in_text:
                in_text = True
                current_text = []
            elif char == ')' and in_text:
                in_text = False
                extracted = ''.join(current_text)
                if len(extracted) > 1 and any(c.isalpha() for c in extracted):
                    text_parts.append(extracted)
            elif in_text:
                current_text.append(char)
    except Exception:
        pass
    
    if text_parts:
        result = ' '.join(text_parts)
        print(f"  > Successfully extracted text from PDF: {os.path.basename(file_path)}")
        print(f"  > Characters extracted: {len(result)}")
        return result
    else:
        raise ValueError(
            "Could not extract text from PDF. "
            "Please ensure it contains selectable text, or paste text directly."
        )


def read_raw_text(text):
    """
    Accept raw text input directly (e.g., from user pasting resume).
    
    Args:
        text (str): Raw resume text
        
    Returns:
        str: Validated text content
    """
    if not text or not text.strip():
        raise ValueError("Resume text is empty")
    
    content = text.strip()
    print(f"  > Raw text input received")
    print(f"  > Characters: {len(content)}")
    return content


def load_resume(source):
    """
    Main entry point — Automatically detects input type and loads resume.
    
    Args:
        source (str): File path (.txt / .pdf) or raw text string
        
    Returns:
        str: Extracted resume text
    """
    print("\n" + "=" * 60)
    print("  MODULE 1: INPUT - Loading Resume")
    print("=" * 60)
    
    # Check if source is a file path
    if os.path.isfile(source):
        ext = os.path.splitext(source)[1].lower()
        if ext == '.txt':
            return read_text_file(source)
        elif ext == '.pdf':
            return read_pdf_file(source)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Use .txt or .pdf")
    
    # Otherwise treat as raw text
    return read_raw_text(source)
