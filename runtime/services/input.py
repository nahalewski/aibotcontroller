import time
from typing import List, Dict, Optional
import sys
import os

# Platform-specific adapters
class BaseInputAdapter:
    def press_key(self, key: str, duration_ms: int = 100):
        pass
    def hold_key(self, key: str):
        pass
    def release_key(self, key: str):
        pass
    def move_mouse(self, dx: int, dy: int):
        pass
    def click_mouse(self, button: str, event: str = "click"):
        pass
    def set_controller_axis(self, axis: str, value: float):
        pass
    def press_controller_button(self, button: str, event: str = "tap"):
        pass

class InputInjectionService:
    def __init__(self):
        self.adapter = self._get_adapter()
        self.last_action_time = 0
        self.action_cooldown = 0.05 # 50ms min between actions
        self.max_actions_per_second = 20

    def _get_adapter(self) -> BaseInputAdapter:
        if sys.platform == "darwin":
            from adapters.macos_input import MacOSInputAdapter
            return MacOSInputAdapter()
        elif sys.platform == "win32":
            from adapters.windows_input import WindowsInputAdapter
            return WindowsInputAdapter()
        else:
            raise NotImplementedError(f"Platform {sys.platform} not supported")

    def execute_actions(self, action_data: Dict):
        """Executes a list of actions from the AI schema."""
        mode = action_data.get("mode", "keyboard_mouse")
        actions = action_data.get("actions", [])
        
        for action in actions:
            # Respect cooldowns and rate limits
            now = time.time()
            if now - self.last_action_time < self.action_cooldown:
                time.sleep(self.action_cooldown)
            
            self._handle_action(action, mode)
            self.last_action_time = time.time()

    def _handle_action(self, action: Dict, mode: str):
        type_ = action.get("type")
        
        if type_ == "key":
            key = action.get("key")
            event = action.get("event", "tap")
            duration = action.get("duration_ms", 100)
            if event == "down":
                self.adapter.hold_key(key)
            elif event == "up":
                self.adapter.release_key(key)
            else: # tap
                self.adapter.press_key(key, duration)
        
        elif type_ == "mouse_move":
            dx = action.get("dx", 0)
            dy = action.get("dy", 0)
            self.adapter.move_mouse(dx, dy)
            
        elif type_ == "mouse_button":
            button = action.get("button", "left")
            event = action.get("event", "click")
            self.adapter.click_mouse(button, event)

        elif type_ in ["left_stick", "right_stick"]:
            x = action.get("x", 0.0)
            y = action.get("y", 0.0)
            prefix = "left_" if type_ == "left_stick" else "right_"
            self.adapter.set_controller_axis(f"{prefix}x", x)
            self.adapter.set_controller_axis(f"{prefix}y", y)

        elif type_ == "button": # controller button
            btn = action.get("button")
            event = action.get("event", "tap")
            self.adapter.press_controller_button(btn, event)
