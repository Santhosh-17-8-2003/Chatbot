import json
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .forms import ChatInputForm
from .models import Message
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key=settings.GEMINI_API_KEY)

try:
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    print("Gemini model initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    gemini_model = None

def get_bot_response(user_message):
    if not gemini_model:
        return "Chat service is currently unavailable. Please check backend configuration."
    try:
        teacher_persona_prompt = (
            "You are an AI assistant role-playing as a knowledgeable, patient, and encouraging teacher "
            "for a school student. Respond to the user's questions and statements as if you are "
            "guiding them, providing clear explanations, asking follow-up questions if appropriate, "
            "and maintaining a supportive tone. Remember to act strictly as a teacher. "
            f"The student's message is: \"{user_message}\""
        )
        response = gemini_model.generate_content(teacher_persona_prompt)

        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            print(f"Gemini API returned an empty or malformed response for message: {user_message}")
            return "Could not get a valid response from the AI. Please try rephrasing."
    except Exception as e:
        print("Gemini API Error during content generation:", e)
        return "There was a problem contacting Gemini. Please try again later."

def chat_view(request):
    form = ChatInputForm()
    messages = []
    context = {
        'form': form,
        'messages': messages,
        'welcome_message': 'Hello! I am your school assistant. How can I help you today?'
    }
    return render(request, 'chat.html', context)

@csrf_exempt
def get_bot_response_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('prompt', '').strip()
            if user_input:
                bot_response = get_bot_response(user_input)
                Message.objects.create(user_message=user_input, bot_response=bot_response)
                return JsonResponse({'bot_response': bot_response})
            return JsonResponse({'error': 'No input provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("Error in get_bot_response_ajax:", e)
            return JsonResponse({'error': 'Server error occurred'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def index(request):
    return chat_view(request)