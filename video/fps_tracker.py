import time
from collections import deque
from config.video_config import DisplayConfig

class FPSTracker:
    def __init__(self):
        self.frame_times = deque(maxlen=DisplayConfig.FPS_SMOOTHING_FACTOR)
        self.last_update_time = time.time()
        self.last_display_time = time.time()

    def update(self) -> None:
        current_time = time.time()

        if len(self.frame_times) > 0:
            self.frame_times.append(current_time)
            avg_frame_time = (self.frame_times[-1] - self.frame_times[0]) / len(self.frame_times)
            fps = 1 / avg_frame_time
        else:
            self.frame_times.append(current_time)
            fps = 0

        if current_time - self.last_display_time >= DisplayConfig.UPDATE_INTERVAL:
            self.displayed_fps = fps
            self.last_display_time = current_time