import os
import sys
import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from classify import classify, classify_log  # Import the single log classifier

sys.path.insert(0, os.path.dirname(__file__))

app = FastAPI(title="Log Classification API")

class LogEntry(BaseModel):
    source: str
    log_message: str


@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    try:
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400,detail="CSV must contain 'source' and 'log_message' columns.")
        
        # perform classification
        df['target_label'] = classify(list(zip(df['source'], df['log_message'])))

        output_file = "Resorces/output.csv"
        df.to_csv(output_file, index=False)

        print("File saved to output.csv")
        
        return FileResponse(output_file,media_type='text/csv')
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    finally:
        file.file.close()

@app.post("/classify/single/")
async def classify_single_log(log_entry: LogEntry):
    """
    Classify a single log entry
    
    Parameters:
    - source: The source system of the log (e.g., 'API', 'System', 'LegacyCRM')
    - log_message: The actual log message to classify
    
    Returns:
    - classification: The predicted classification label for the log
    """
    try:
        result = classify_log(log_entry.source, log_entry.log_message)
        return {"Label": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    