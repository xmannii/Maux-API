from docx import Document
import io

async def extract(file):
    try:
        content = await file.read()
        doc_file = io.BytesIO(content)
        document = Document(doc_file)
        
        full_text = []
        for para in document.paragraphs:
            full_text.append(para.text)
        
        return "\n".join(full_text)
    except Exception as e:
        raise Exception(f"Error extracting DOC content: {str(e)}")