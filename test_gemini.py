import google.generativeai as genai

genai.configure(api_key="AIzaSyAWGxn2orFXQLBcVwjS7R8pb3fya8_q7Hk")

models = genai.list_models()
for m in models:
    print(m.name, " | ", m.supported_generation_methods)

model = genai.GenerativeModel(model_name="gemini-pro")
response = model.generate_content("Who is the president of India?")
print(response.text)