import io
from typing import List, Dict, Tuple
import fitz
from langchain_core.documents import Document

def extract_text_from_pdf(pdf_bytes: bytes, filename: str) -> Tuple[List[Document], Dict[str, any]]:
    documents = []
    metadata = {
        "filename": filename,
        "total_pages": 0,
        "total_text_length": 0
    }
    
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        metadata["total_pages"] = pdf_document.page_count
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            
            text = clean_text(text)
            
            if text.strip():
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": filename,
                        "page": page_num + 1,
                        "total_pages": pdf_document.page_count
                    }
                )
                documents.append(doc)
                metadata["total_text_length"] += len(text)
        
        pdf_document.close()
        
    except Exception as e:
        raise Exception(f"Error processing PDF {filename}: {str(e)}")
    
    return documents, metadata

def clean_text(text: str) -> str:
    text = text.replace('\x00', '')
    
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = ' '.join(line.split())
        if line:
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    text = text.strip()
    
    return text

def process_multiple_pdfs(uploaded_files) -> Tuple[List[Document], List[Dict[str, any]]]:
    all_documents = []
    all_metadata = []
    
    for uploaded_file in uploaded_files:
        try:
            pdf_bytes = uploaded_file.read()
            
            documents, metadata = extract_text_from_pdf(pdf_bytes, uploaded_file.name)
            all_documents.extend(documents)
            all_metadata.append(metadata)
            
        except Exception as e:
            all_metadata.append({
                "filename": uploaded_file.name,
                "error": str(e),
                "total_pages": 0,
                "total_text_length": 0
            })
    
    return all_documents, all_metadata
