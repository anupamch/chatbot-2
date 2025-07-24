import traceback
from fastapi import FastAPI
import json
from datetime import datetime
from pathlib import Path
import numpy as np
from transformers import pipeline, AutoTokenizer
from accelerate import Accelerator
import torch
import psutil
import time
from typing import Dict, Any
from pydentic_class.pydentic import PromptRequest, GenerationResponse, SystemStatus
# Initialize FastAPI app
app = FastAPI(title="Local LLM API")


# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Using device: {device}")
# Initialize accelerator for better performance
accelerator = Accelerator()

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("gpt2")
# Set pad_token to eos_token if it doesn't exist
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token
    
model = pipeline(
    "text-generation",
    model="gpt2",
    tokenizer=tokenizer,
    device=accelerator.device,
    truncation=True,
    max_new_tokens=50
)  # Using GPT-2 as an example





Path("logs").mkdir(exist_ok=True)

def log_interaction(prompt: str, response: str):
    """Log the prompt and response to a JSON file"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "prompt": prompt,
        "response": response
    }
    
    log_file = Path("logs") / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    
    
    if log_file.exists():
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    
    
    logs.append(log_entry)
    
    # Write back to file
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

@app.post("/generate", response_model=GenerationResponse)
async def generate_response(request: PromptRequest):
    # Generate response using the model
    error = False
    try:
        generated = model(request.prompt,
            max_new_tokens=50,
            num_return_sequences=1,
            pad_token_id=model.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7)[0]
        response = generated["generated_text"]
    except Exception as e:
        error = True
        print(traceback.format_exc())
        response = "I'm a local AI model, running offline!"
    
    # Log the interaction
    log_interaction(request.prompt, response)
    
    return GenerationResponse(response=response, error=error)
    
@app.get("/status", response_model=SystemStatus)
async def get_status():
    
    device_info = {
        "device": str(accelerator.device),
        "cuda_available": str(torch.cuda.is_available()),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU",
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A"
    }
    
    
    memory_info = psutil.virtual_memory()
    memory_usage = {
        "total_gb": memory_info.total / (1024 ** 3),
        "available_gb": memory_info.available / (1024 ** 3),
        "percent_used": memory_info.percent
    }
    
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory
        memory_usage["gpu_total_gb"] = gpu_memory / (1024 ** 3)
        memory_usage["gpu_allocated_gb"] = torch.cuda.memory_allocated(0) / (1024 ** 3)
    return SystemStatus(
        device_info=device_info,
        memory_usage=memory_usage,
        model_info={
            "model_name": "gpt2",
            "max_tokens": 50,
            "tokenizer_vocab_size": len(tokenizer),
            "using_accelerate": True
        }
    )


@app.get("/")
async def root():
    return {"message": "Welcome to the Local LLM API"}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
