import PyPDF2
import io
from app.models.extraction_models import ExtractedContent

async def extract(file):
    try:
        content = await file.read()
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        extracted_content = []
        for page_number, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:  # Only add if text is not None
                extracted_content.append(ExtractedContent(text=text.strip(), page_number=page_number + 1))
        
        return extracted_content
    except Exception as e:
        raise Exception(f"Error extracting PDF content: {str(e)}")