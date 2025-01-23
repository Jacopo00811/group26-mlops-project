# import logging

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# logger = logging.getLogger(__name__)

# app = FastAPI()


# class TranslationRequest(BaseModel):
#     danish_text: str


# class TranslationResponse(BaseModel):
#     english_text: str


# @app.post("/translate/", response_model=TranslationResponse)
# async def translate_text(request: TranslationRequest):
#     """Echo the input text (for testing purposes only)."""
#     try:
#         # Simply return the same text that was input
#         return TranslationResponse(english_text=request.danish_text)
#     except Exception as e:
#         logger.error(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail="Error processing text")




# import logging

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# import onnxruntime

# logger = logging.getLogger(__name__)

# app = FastAPI()

# # Load model
# try:
#     model = onnxruntime.InferenceSession("models/model.onnx")
#     logger.info("Model loaded successfully")

# except FileNotFoundError:
#     logger.warning("Model not found.")
# class TranslationRequest(BaseModel):
#     danish_text: str


# class TranslationResponse(BaseModel):
#     english_text: str


# @app.post("/translate/", response_model=TranslationResponse)
# async def translate_text(request: TranslationRequest):
#     """Translate Danish text to English."""
#     try:
#         danish_text = request.danish_text
#         english_text = model.run(None, danish_text)
#         english_text = english_text[0].tolist()
#         return TranslationResponse(english_text=english_text)
#     except Exception as e:
#         logger.error(f"Error translating text: {e}")
#         raise HTTPException(status_code=500, detail="Error translating text")


import logging
import numpy as np
import onnxruntime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import T5Tokenizer

logger = logging.getLogger(__name__)

app = FastAPI()

# Load model and tokenizer
try:
    session = onnxruntime.InferenceSession("models/model.onnx")
    
    tokenizer = T5Tokenizer.from_pretrained("google-t5/t5-small")
    
    input_names = [input.name for input in session.get_inputs()]
    output_name = session.get_outputs()[0].name
    
    logger.info("Model loaded successfully")

except FileNotFoundError:
    logger.warning("Model not found.")

class TranslationRequest(BaseModel):
    danish_text: str

class TranslationResponse(BaseModel):
    english_text: str

@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate Danish text to English."""
    try:
        danish_text = request.danish_text
        
        # Tokenize input
        inputs = tokenizer(danish_text, return_tensors="np", padding=True, truncation=True)
        
        # Prepare all required inputs
        input_feed = {
            'input_ids': inputs['input_ids'],
            'attention_mask': inputs['attention_mask'],
            'decoder_input_ids': np.zeros_like(inputs['input_ids'], dtype=np.int64)
        }
        
        # Run inference with all inputs
        result = session.run([output_name], input_feed)
        
        # Handle potential 0-dimensional array
        if result[0].ndim == 0:
            english_text = tokenizer.decode(result[0], skip_special_tokens=True)
        else:
            english_text = tokenizer.decode(result[0][0], skip_special_tokens=True)
        
        return TranslationResponse(english_text=english_text)
    
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        raise HTTPException(status_code=500, detail=f"Error translating text: {str(e)}")