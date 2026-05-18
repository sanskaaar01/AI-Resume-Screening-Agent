import google.generativeai as genai

genai.configure(api_key="AIzaSyD2Qj-9ON7C1NVq1bCOuHTAeqwO7UI08I4")

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Hello")

print(response.text)