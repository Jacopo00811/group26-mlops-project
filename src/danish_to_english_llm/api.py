import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer

# Set up logging
logging.basicConfig(level=logging.INFO)

# FastAPI instance
app = FastAPI()

# Load translation model and tokenizer for Danish-to-English
model_name = "Helsinki-NLP/opus-mt-en-da"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


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

        # Tokenize the formatted input text
        inputs = tokenizer(input_prompt, return_tensors="pt", padding=True, truncation=True)

        # Generate the output (translation)
        output = model.generate(inputs["input_ids"], max_length=50)

        # Decode the output
        processed_text = tokenizer.decode(output[0], skip_special_tokens=True)

        logging.info(f"Processed text: {processed_text}")

        # Return the processed text (translated output)
        return {"text": processed_text}

    except Exception as e:
        logging.error(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
