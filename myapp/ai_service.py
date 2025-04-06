import os
import requests
import json
from django.conf import settings
api_key = getattr(settings, "GROQ_API_KEY", "")


class GroqAIService:
    def __init__(self):
        self.api_key = getattr(settings, "GROQ_API_KEY", "")
        self.api_key = os.environ.get("GROQ_API_KEY", "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")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
    def generate_response(self, user_message, model="llama3-8b-8192"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an AI fitness trainer assistant. Provide helpful, accurate, and motivational advice about exercises, nutrition, and overall fitness."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"