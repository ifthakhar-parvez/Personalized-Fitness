from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def nutrition_index (request):
    return render(request, 'meals/nutrition_index.html')

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Optional reset command
        if user_message.strip().lower() in ["reset", "restart", "clear"]:
            request.session.flush()
            return JsonResponse({
                "response": "Okay, let's start fresh! How can I help you with your nutrition today?"
            })

        # Initialize chat history in session
        if "chat_history" not in request.session:
            request.session["chat_history"] = []
            request.session["conversation_started"] = True

        chat_history = request.session["chat_history"]

        # Include the last 5 exchanges in the prompt
        instruction_blocks = ""
        for exchange in chat_history[-5:]:
            instruction_blocks += f"### Instruction:\n{exchange['user']}\n\n### Response:\n{exchange['bot']}\n\n"

        # Add current message to the prompt
        instruction_blocks += f"### Instruction:\n{user_message}\n\n### Response:\n"

        # Hugging Face API setup
        api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
        }
        payload = {
            "inputs": instruction_blocks
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)

            if response.status_code == 200:
                try:
                    result = response.json()
                    raw_text = result[0].get("generated_text", "")
                    if "### Response:" in raw_text:
                        bot_message = raw_text.split("### Response:")[-1].strip()
                    else:
                        bot_message = raw_text.strip()
                except Exception:
                    bot_message = "Sorry, the model returned an unexpected response."
            else:
                bot_message = f"Error {response.status_code}: {response.text}"

        except Exception as e:
            bot_message = f"Error: {str(e)}"

        # Save the latest exchange
        chat_history.append({"user": user_message, "bot": bot_message})
        request.session["chat_history"] = chat_history

        return JsonResponse({"response": bot_message})