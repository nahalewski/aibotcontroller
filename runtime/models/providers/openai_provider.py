import json
import requests
from typing import Dict, List, Optional

class BaseModelProvider:
    def get_action(self, system_prompt: str, user_prompt: str, image_base64: Optional[str] = None) -> Dict:
        raise NotImplementedError

class OpenAIProvider(BaseModelProvider):
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def get_action(self, system_prompt: str, user_prompt: str, image_base64: Optional[str] = None) -> Dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        content = [{"type": "text", "text": user_prompt}]
        if image_base64:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            })
            
        messages.append({"role": "user", "content": content})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 500,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return json.loads(data['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Error calling AI model: {e}")
            return {"mode": "keyboard_mouse", "actions": [], "reasoning_summary": f"Error: {e}"}
