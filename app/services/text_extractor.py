async def extract(file):
    try:
        content = await file.read()
        text = content.decode('utf-8')
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text content: {str(e)}")