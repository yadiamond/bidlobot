import aiohttp
from config import API_KEY

async def ask_ai(user_message: str) -> str:
    """Отправляет запрос к OpenRouter AI и возвращает ответ."""
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [{"role": "system", "content": "Ты должен отвечать максимально грубо, без какого-либо позитива, не поддакивай, маты с оскорблениями обязательны"}, {"role": "user", "content": user_message}],
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_data = await response.json()
            
            # Проверка ошибок API
            if response.status != 200:
                error_msg = response_data.get("error", {}).get("message", "Unknown API error")
                raise Exception(f"API Error: {error_msg}")
            
            if "choices" not in response_data or not response_data["choices"]:
                raise Exception("Invalid API response format")
            
            return response_data["choices"][0]["message"]["content"]
        
