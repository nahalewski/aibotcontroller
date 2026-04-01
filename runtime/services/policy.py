import json
from typing import Dict, List, Optional
from models.providers.openai_provider import OpenAIProvider

class PolicyService:
    def __init__(self):
        self.provider = None
        self.system_prompt = (
            "You are GamePilot AI, a gaming assistant. Observe the game state and decide on the best "
            "short-term actions. Output JSON only according to the schema provided. "
            "Never assume hidden data. Avoid repeating failed actions."
        )
        self.action_schema = {
            "type": "object",
            "properties": {
                "mode": {"enum": ["keyboard_mouse", "controller"]},
                "actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "oneOf": [
                            {"properties": {"type": {"const": "key"}, "key": {"type": "string"}, "event": {"enum": ["down", "up", "tap"]}, "duration_ms": {"type": "integer"}}},
                            {"properties": {"type": {"const": "mouse_move"}, "dx": {"type": "integer"}, "dy": {"type": "integer"}}},
                            {"properties": {"type": {"const": "mouse_button"}, "button": {"enum": ["left", "right"]}, "event": {"enum": ["click", "down", "up"]}}}
                        ]
                    }
                },
                "reasoning_summary": {"type": "string"}
            }
        }

    def configure_provider(self, provider_type: str, config: Dict):
        if provider_type == "openai":
            self.provider = OpenAIProvider(
                api_key=config.get("api_key"),
                base_url=config.get("base_url", "https://api.openai.com/v1"),
                model=config.get("model", "gpt-4o")
            )
        else:
            raise NotImplementedError(f"Provider {provider_type} not supported")

    def decide_action(self, state: Dict, image_base64: Optional[str] = None) -> Dict:
        """Sends state to AI model and returns a validated action JSON."""
        if not self.provider:
            return {"mode": "keyboard_mouse", "actions": [], "reasoning_summary": "No provider configured"}

        user_prompt = f"Current structured state: {json.dumps(state)}. Decide the next best action."
        
        # In a real scenario, we'd include more context from the game profile here.
        action = self.provider.get_action(self.system_prompt, user_prompt, image_base64)
        
        # Simple validation
        if not isinstance(action, dict) or "actions" not in action:
            return {"mode": "keyboard_mouse", "actions": [], "reasoning_summary": "Invalid action format from AI"}
            
        return action
