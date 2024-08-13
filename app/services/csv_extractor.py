import pandas as pd
import io

async def extract(file):
    try:
        content = await file.read()
        csv_file = io.StringIO(content.decode('utf-8'))
        df = pd.read_csv(csv_file)

        records = df.to_dict('records')
        
        return records
    except Exception as e:
        raise Exception(f"Error extracting CSV content: {str(e)}")