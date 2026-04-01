import cv2
import numpy as np
from typing import Dict, List, Optional
import pytesseract

class PerceptionService:
    def __init__(self):
        self.enabled_ocr = False
        self.crop_regions = {} # e.g. {"minimap": [0, 0, 100, 100]}

    def process_frame(self, frame: np.ndarray) -> Dict:
        """Processes a frame to extract a structured state."""
        state = {
            "timestamp": cv2.getTickCount(),
            "text_elements": [],
            "objects": []
        }
        
        if self.enabled_ocr:
            # Grayscale for OCR
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Resize for better OCR results?
            # data = pytesseract.image_to_string(gray)
            # state["text_elements"].append(data)
            pass

        return state

    def set_ocr_enabled(self, enabled: bool):
        self.enabled_ocr = enabled
