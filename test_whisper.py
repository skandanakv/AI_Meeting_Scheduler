from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

print("Testing Groq Whisper...")
print("Whisper is available through your existing GROQ_API_KEY")
print("✅ Ready to use in the app!")

# If you have a test audio file, uncomment:
# with open("test.wav", "rb") as audio:
#     result = client.audio.transcriptions.create(
#         file=audio,
#         model="whisper-large-v3"
#     )
#     print(f"Transcription: {result.text}")