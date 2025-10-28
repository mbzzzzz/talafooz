from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/abdulwaheed1/english-to-urdu-translation-mbart"
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def translate_text(text):
    """Translate English text to Urdu using Hugging Face API"""
    if not HF_API_TOKEN:
        return {"error": "Hugging Face API token not configured"}
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 512,
            "num_beams": 4,
            "early_stopping": True
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return {"translation": result[0].get("translated_text", "")}
        else:
            return {"error": "No translation received"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Translation failed: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({"error": "No text provided"})
    
    result = translate_text(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
