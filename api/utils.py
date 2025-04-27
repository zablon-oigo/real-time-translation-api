import os
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session
from query import update_translation_task

load_dotenv()

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.getenv("GITHUB_TOKEN"),
)

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}
    for lang in languages:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4.1",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant who translates text to {lang}."},
                    {"role": "user", "content": text},
                ],
                temperature=1.0,
                top_p=1.0,
            )
            translated = response.choices[0].message.content.strip()
            translations[lang] = translated
        except Exception as e:
            print(f"[Translation error] {lang}: {e}")
            translations[lang] = f"Error: {e}"
    update_translation_task(db, task_id, translations)





