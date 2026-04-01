import mss
import mss.tools
import numpy as np
import cv2
import pywinctl as pwc
import time
from typing import List, Optional, Tuple

class CaptureService:
    def __init__(self):
        self.sct = mss.mss()
        self.current_window = None
        self.current_monitor = None
        self.fps_limit = 15
        self.scale = 1.0
        self.last_capture_time = 0

    def get_windows(self) -> List[dict]:
        """Returns a list of visible windows with titles and IDs."""
        windows = pwc.getAllWindows()
        return [{"id": w.getHandle(), "title": w.title} for w in windows if w.title]

    def get_monitors(self) -> List[dict]:
        """Returns a list of available monitors."""
        return [{"id": i, "name": f"Monitor {i}"} for i, monitor in enumerate(self.sct.monitors)]

    def select_window(self, window_title: str):
        windows = pwc.getWindowsWithTitle(window_title)
        if windows:
            self.current_window = windows[0]
            self.current_monitor = None
            return True
        return False

    def select_monitor(self, monitor_id: int):
        if 0 <= monitor_id < len(self.sct.monitors):
            self.current_monitor = self.sct.monitors[monitor_id]
            self.current_window = None
            return True
        return False

    def capture_frame(self) -> Optional[np.ndarray]:
        """Captures a frame based on current selection."""
        now = time.time()
        if now - self.last_capture_time < (1.0 / self.fps_limit):
             return None # Skip to maintain FPS limit
        
        self.last_capture_time = now

        if self.current_window:
            # Refresh window position
            if not self.current_window.isActive:
                # Should we activate it? 
                pass
            
            rect = {
                "top": self.current_window.top,
                "left": self.current_window.left,
                "width": self.current_window.width,
                "height": self.current_window.height,
            }
            img = self.sct.grab(rect)
        elif self.current_monitor:
            img = self.sct.grab(self.current_monitor)
        else:
            # Default to primary monitor
            img = self.sct.grab(self.sct.monitors[1])

        # Convert to numpy array (BGRA to BGR)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        if self.scale != 1.0:
            width = int(frame.shape[1] * self.scale)
            height = int(frame.shape[0] * self.scale)
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        return frame

    def encode_frame(self, frame: np.ndarray) -> str:
        """Encodes frame to base64 for transmission."""
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        import base64
        return base64.b64encode(buffer).decode('utf-8')
