import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI()


class TranslationRequest(BaseModel):
    danish_text: str


class TranslationResponse(BaseModel):
    english_text: str


@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Echo the input text (for testing purposes only)."""
    try:
        # Simply return the same text that was input
        return TranslationResponse(english_text=request.danish_text)
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail="Error processing text")


# import logging

# import torch
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# from .model import T5LightningModel

# logger = logging.getLogger(__name__)

# app = FastAPI()

# # Load model
# try:
#     try:
#         model = T5LightningModel.load_from_checkpoint("models/final_model.pth")
#     except FileNotFoundError:
#         logger.warning("Model not found. Training new model...")
#         model = T5LightningModel()
#         model.train()
#         model.save_model("models/final_model.pth")

#     model.eval()
#     logger.info("Model loaded successfully")

# except Exception as e:
#     logger.error(f"Error initializing model: {e}")
#     raise RuntimeError("Failed to initialize model")


# class TranslationRequest(BaseModel):
#     danish_text: str


# class TranslationResponse(BaseModel):
#     english_text: str


# @app.post("/translate/", response_model=TranslationResponse)
# async def translate_text(request: TranslationRequest):
#     """Translate Danish text to English."""
#     try:
#         danish_text = request.danish_text
#         english_text = model.translate(danish_text)
#         return TranslationResponse(english_text=english_text)
#     except Exception as e:
#         logger.error(f"Error translating text: {e}")
#         raise HTTPException(status_code=500, detail="Error translating text")
