from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.extraction_models import ExtractionResponse, ExtractedContent
from app.services import pdf_extractor, csv_extractor, doc_extractor, text_extractor
from app.services.word_count_service import count_words, process_content
from app.utils.file_utils import get_file_extension
from datetime import datetime
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/extract", response_model=ExtractionResponse)
async def extract_content(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    logger.info(f"Received file: {file.filename}")
    file_extension = get_file_extension(file.filename)
    
    supported_extensions = {".pdf", ".csv", ".doc", ".docx", ".txt", ".md"}
    
    if file_extension not in supported_extensions:
        logger.warning(f"Unsupported file type: {file_extension}")
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
    
    try:
        extraction_start = datetime.now()
        
        if file_extension == ".pdf":
            content = await pdf_extractor.extract(file)
        elif file_extension == ".csv":
            content = await csv_extractor.extract(file)
        elif file_extension in [".doc", ".docx"]:
            content = await doc_extractor.extract(file)
        elif file_extension in [".txt", ".md"]:
            content = await text_extractor.extract(file)
        
        extraction_end = datetime.now()
        extraction_duration = extraction_end - extraction_start
        
        # Process the extracted content
        total_word_count = sum(len(page.text.split()) for page in content)  # Count words in all pages
        
        logger.info(f"Successfully extracted content from {file.filename}")
        
        return ExtractionResponse(
            filename=file.filename,
            file_type=file_extension,
            extraction_time=extraction_duration,
            word_count=total_word_count,
            content=content  # This is now a list of ExtractedContent
        )
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")