import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent"

class Assistents:

    def __init__(self):
        pass

    def generate_text(self, API_KEY, text):
        
        data = {
            "contents": [{
                "parts": [{
                    "text": text
                }]
            }]
        }

        response = requests.post(f"{API_URL}?key={API_KEY}", json=data)

        if response.status_code == 200:
            try:
                generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                return generated_text
            except KeyError:
                print("Resposta inesperada da API:", response.json())
                return ""
        else:
            print("Erro na requisição:", response.status_code, response.json())
            return ""