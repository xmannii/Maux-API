from typing import List, Union
from app.models.extraction_models import ExtractedContent

def count_words(content: Union[str, List[Union[str, dict]]]) -> int:
    total_word_count = 0

    if isinstance(content, str):
        total_word_count = len(content.split())
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                text = item.get('text', '')
            elif isinstance(item, str):
                text = item
            else:
                text = str(item)
            total_word_count += len(text.split())

    return total_word_count

def process_content(content: Union[str, List[Union[str, dict]]]) -> List[ExtractedContent]:
    processed_content = []

    if isinstance(content, list):
        for idx, item in enumerate(content, start=1):
            if isinstance(item, dict):
                text = item.get('text', '')
                metadata = {k: v for k, v in item.items() if k != 'text'}
                processed_content.append(ExtractedContent(
                    text=text,
                    page_number=idx,
                    metadata=metadata
                ))
            else:
                processed_content.append(ExtractedContent(text=str(item), page_number=idx))
    else:
        processed_content.append(ExtractedContent(text=str(content)))

    return processed_content