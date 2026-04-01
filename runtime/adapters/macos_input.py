import Quartz.CoreGraphics as CG
import time
from typing import Dict

# Key mapping from string to Quartz virtual key codes
# (Partial list for V1, needs expansion)
KEY_MAP = {
    'w': 13, 'a': 0, 's': 1, 'd': 2,
    'e': 14, 'q': 12, 'r': 15, 't': 17,
    'space': 49, 'shift': 56, 'ctrl': 59, 'alt': 58,
    'up': 126, 'down': 125, 'left': 123, 'right': 124,
    'enter': 36, 'esc': 53,
}

class MacOSInputAdapter:
    def __init__(self):
        pass

    def _get_key_code(self, key: str) -> int:
        return KEY_MAP.get(key.lower(), 0)

    def press_key(self, key: str, duration_ms: int = 100):
        code = self._get_key_code(key)
        self.hold_key(key)
        time.sleep(duration_ms / 1000.0)
        self.release_key(key)

    def hold_key(self, key: str):
        code = self._get_key_code(key)
        event = CG.CGEventCreateKeyboardEvent(None, code, True)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

    def release_key(self, key: str):
        code = self._get_key_code(key)
        event = CG.CGEventCreateKeyboardEvent(None, code, False)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

    def move_mouse(self, dx: int, dy: int):
        # Quartz mouse move using delta
        # First get current position
        event = CG.CGEventCreate(None)
        loc = CG.CGEventGetLocation(event)
        
        new_loc = (loc.x + dx, loc.y + dy)
        move = CG.CGEventCreateMouseEvent(None, CG.kCGEventMouseMoved, new_loc, 0)
        CG.CGEventPost(CG.kCGHIDEventTap, move)

    def click_mouse(self, button: str, event: str = "click"):
        # Get current pos
        e = CG.CGEventCreate(None)
        loc = CG.CGEventGetLocation(e)
        
        btn_map = {
            "left": (CG.kCGEventLeftMouseDown, CG.kCGEventLeftMouseUp),
            "right": (CG.kCGEventRightMouseDown, CG.kCGEventRightMouseUp)
        }
        
        down_type, up_type = btn_map.get(button, btn_map["left"])
        
        if event == "down" or event == "click":
            down = CG.CGEventCreateMouseEvent(None, down_type, loc, CG.kCGMouseButtonLeft if button == "left" else CG.kCGMouseButtonRight)
            CG.CGEventPost(CG.kCGHIDEventTap, down)
        
        if event == "up" or event == "click":
            up = CG.CGEventCreateMouseEvent(None, up_type, loc, CG.kCGMouseButtonLeft if button == "left" else CG.kCGMouseButtonRight)
            CG.CGEventPost(CG.kCGHIDEventTap, up)

    def set_controller_axis(self, axis: str, value: float):
        # macOS stub for virtual controller
        print(f"Controller Axis Stub: {axis} = {value}")

    def press_controller_button(self, button: str, event: str = "tap"):
        # macOS stub for virtual controller
        print(f"Controller Button Stub: {button} = {event}")
