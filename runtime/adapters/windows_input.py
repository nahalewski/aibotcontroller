import ctypes
import time
import sys

# Windows Constants and Structs for SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Flag Constants
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

# Scan codes (DirectX relies on these)
SCAN_CODES = {
    'w': 0x11, 'a': 0x1E, 's': 0x1F, 'd': 0x20,
    'e': 0x12, 'q': 0x10, 'r': 0x13, 't': 0x14,
    'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38,
    'enter': 0x1C, 'esc': 0x01
}

class WindowsInputAdapter:
    def __init__(self):
        self.gamepad = None
        try:
            import vgamepad as vg
            self.gamepad = vg.VX360Gamepad()
        except ImportError:
            print("vgamepad not installed, controller support disabled")

    def press_key(self, key: str, duration_ms: int = 100):
        self.hold_key(key)
        time.sleep(duration_ms / 1000.0)
        self.release_key(key)

    def hold_key(self, key: str):
        scan_code = SCAN_CODES.get(key.lower(), 0)
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, scan_code, 0x0008, 0, ctypes.pointer(extra)) # 0x0008 = KEYEVENTF_SCANCODE
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def release_key(self, key: str):
        scan_code = SCAN_CODES.get(key.lower(), 0)
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, scan_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def move_mouse(self, dx: int, dy: int):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def click_mouse(self, button: str, event: str = "click"):
        btn_map = {
            "left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
            "right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP)
        }
        down_flag, up_flag = btn_map.get(button, btn_map["left"])
        
        extra = ctypes.c_ulong(0)
        
        if event == "down" or event == "click":
            ii_ = Input_I()
            ii_.mi = MouseInput(0, 0, 0, down_flag, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        if event == "up" or event == "click":
            ii_ = Input_I()
            ii_.mi = MouseInput(0, 0, 0, up_flag, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def set_controller_axis(self, axis: str, value: float):
        if not self.gamepad: return
        import vgamepad as vg
        if axis == "left_x": self.gamepad.left_joystick_float(x_value_float=value, y_value_float=self.gamepad.get_left_y())
        elif axis == "left_y": self.gamepad.left_joystick_float(x_value_float=self.gamepad.get_left_x(), y_value_float=value)
        # Update...
        self.gamepad.update()

    def press_controller_button(self, button: str, event: str = "tap"):
        if not self.gamepad: return
        # Map button and apply...
        self.gamepad.update()
