from google import genai

client = genai.Client(
    api_key = "AIzaSyAT1GORgiuFXlmOticsOj6YRo2Reme9kTc"
)

def ask_ai(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    return response.text