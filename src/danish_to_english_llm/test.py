import numpy as np
import onnxruntime
from transformers import T5Tokenizer

def query_model(text):
    # Load tokenizer
    tokenizer = T5Tokenizer.from_pretrained("google-t5/t5-small")
    
    # Load ONNX model
    session = onnxruntime.InferenceSession("models/model.onnx")
    
    # Get input and output names
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    # Tokenize input
    inputs = tokenizer(text, return_tensors="np", padding=True, truncation=True)
    
    # Prepare inputs
    input_feed = {
        'input_ids': inputs['input_ids'],
        'attention_mask': inputs['attention_mask'],
        'decoder_input_ids': np.zeros_like(inputs['input_ids'], dtype=np.int64)
    }
    
    # Run inference
    result = session.run([output_name], input_feed)
    
    # Decode output
    if result[0].ndim == 0:
        translation = tokenizer.decode(result[0], skip_special_tokens=True)
    else:
        translation = tokenizer.decode(result[0][0], skip_special_tokens=True)
    
    return translation

# Example usage
if __name__ == "__main__":
    danish_text = input("Enter Danish text to translate: ")
    translation = query_model(danish_text)
    print("\nTranslation:", translation)