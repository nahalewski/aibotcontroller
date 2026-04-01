import time
import asyncio
import threading
from typing import Dict, Optional, Callable
import traceback

from services.capture import CaptureService
from services.perception import PerceptionService
from services.policy import PolicyService
from services.input import InputInjectionService

class CoordinatorService:
    def __init__(self):
        self.capture = CaptureService()
        self.perception = PerceptionService()
        self.policy = PolicyService()
        self.input = InputInjectionService()
        
        self.is_running = False
        self.is_paused = False
        self.loop_thread = None
        self.metrics = {
            "fps": 0,
            "latency_ms": 0,
            "last_action": None
        }
        self.on_frame_callback: Optional[Callable] = None
        self.on_status_callback: Optional[Callable] = None

    def start(self, config: Dict):
        """Starts the control loop."""
        if self.is_running: return
        
        # Configure services based on UI config
        # (e.g. self.policy.configure_provider(...))
        
        self.is_running = True
        self.is_paused = False
        self.loop_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.loop_thread.start()
        print("Coordinator: Loop started")

    def stop(self):
        """Stops the control loop and releases all inputs."""
        self.is_running = False
        if self.loop_thread:
            self.loop_thread.join(timeout=1.0)
        # TODO: self.input.release_all() for safety
        print("Coordinator: Loop stopped")

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def _run_loop(self):
        print("Coordinator: Entering loop thread")
        while self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                continue
            
            start_time = time.time()
            try:
                # 1. Capture
                frame = self.capture.capture_frame()
                if frame is None:
                    continue # Respect FPS limit

                # 2. Perception (Optional)
                state = self.perception.process_frame(frame)
                
                # 3. Policy (AI Decision)
                # For high performance, we might sample frames or skip here
                # Convert frame for AI
                image_b64 = self.capture.encode_frame(frame)
                action_data = self.policy.decide_action(state, image_b64)
                
                # 4. Input Injection
                self.input.execute_actions(action_data)
                
                # 5. Metrics
                loop_duration = time.time() - start_time
                self.metrics["latency_ms"] = int(loop_duration * 1000)
                self.metrics["last_action"] = action_data.get("reasoning_summary")
                
                # Callbacks for live UI updates
                if self.on_frame_callback:
                    self.on_frame_callback(image_b64, self.metrics)

            except Exception as e:
                print(f"Loop error: {e}")
                traceback.print_exc()
                time.sleep(1.0) # Error cooldown

    def get_status(self) -> Dict:
        return {
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "metrics": self.metrics,
            "selected_window": self.capture.current_window.title if self.capture.current_window else "None"
        }
