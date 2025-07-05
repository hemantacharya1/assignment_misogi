import io
import streamlit as st
from typing import Optional

try:
    import pdfplumber
    PDF_PLUMBER_AVAILABLE = True
except ImportError:
    PDF_PLUMBER_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

class PDFProcessor:
    """Handles PDF text extraction using multiple backends."""
    
    def __init__(self):
        self.preferred_backend = self._get_preferred_backend()
    
    def _get_preferred_backend(self) -> str:
        """Determine which PDF processing backend to use."""
        if PDF_PLUMBER_AVAILABLE:
            return 'pdfplumber'
        elif PYMUPDF_AVAILABLE:
            return 'pymupdf'
        else:
            raise ImportError("Neither pdfplumber nor PyMuPDF is available. Please install one of them.")
    
    def extract_text(self, uploaded_file) -> str:
        """Extract text from uploaded PDF file."""
        try:
            if self.preferred_backend == 'pdfplumber':
                return self._extract_with_pdfplumber(uploaded_file)
            elif self.preferred_backend == 'pymupdf':
                return self._extract_with_pymupdf(uploaded_file)
            else:
                raise ValueError(f"Unsupported backend: {self.preferred_backend}")
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def _extract_with_pdfplumber(self, uploaded_file) -> str:
        """Extract text using pdfplumber."""
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            st.error(f"Error with pdfplumber: {str(e)}")
        return text.strip()
    
    def _extract_with_pymupdf(self, uploaded_file) -> str:
        """Extract text using PyMuPDF."""
        text = ""
        try:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text() + "\n"
            pdf_document.close()
        except Exception as e:
            st.error(f"Error with PyMuPDF: {str(e)}")
        return text.strip()
    
    def get_pdf_info(self, uploaded_file) -> dict:
        """Get metadata information about the PDF."""
        try:
            if self.preferred_backend == 'pdfplumber':
                return self._get_info_pdfplumber(uploaded_file)
            elif self.preferred_backend == 'pymupdf':
                return self._get_info_pymupdf(uploaded_file)
        except Exception as e:
            st.error(f"Error getting PDF info: {str(e)}")
            return {}
    
    def _get_info_pdfplumber(self, uploaded_file) -> dict:
        """Get PDF info using pdfplumber."""
        info = {}
        try:
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                info['pages'] = len(pdf.pages)
                info['metadata'] = pdf.metadata or {}
        except Exception as e:
            st.error(f"Error getting PDF info with pdfplumber: {str(e)}")
        return info
    
    def _get_info_pymupdf(self, uploaded_file) -> dict:
        """Get PDF info using PyMuPDF."""
        info = {}
        try:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            info['pages'] = pdf_document.page_count
            info['metadata'] = pdf_document.metadata
            pdf_document.close()
        except Exception as e:
            st.error(f"Error getting PDF info with PyMuPDF: {str(e)}")
        return info 