import logging
import os
from typing import Any, Dict

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import T5TokenizerFast

from danish_to_english_llm.model import T5LightningModel

# Set up logging
logging.basicConfig(level=logging.INFO)

# FastAPI instance
app = FastAPI()

# Load translation model and tokenizer for Danish-to-English
model_name = "google-t5/t5-small"
tokenizer = T5TokenizerFast.from_pretrained(model_name)
if os.path.exists("models/final_model.pth"):
    state_dict = torch.load("models/final_model.pth", weights_only=True)
elif os.path.exists("/gcs/group26_mlops_data_bucket/models/final_model.pth"):
    state_dict = torch.load("/gcs/group26_mlops_data_bucket/models/final_model.pth", weights_only=True)
model = T5LightningModel()
model.load_state_dict(state_dict)


class TextRequest(BaseModel):
    text: str


# API endpoint to process text
@app.post("/process-text/")
async def process_text(request: TextRequest) -> Dict[str, Any]:
    try:
        # Get input text from request
        input_text = request.text
        logging.info(f"Processing text: {input_text}")

        # Format the input text for translation task
        input_prompt = f"translate English to Danish: {input_text}"
        processed_text = model.translate(input_prompt)

        logging.info(f"Processed text: {processed_text}")

        # Return the processed text (translated output)
        return {"text": processed_text}

    except Exception as e:
        logging.error(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
