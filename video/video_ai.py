import os
import time
from queue import Queue
from threading import Lock, Thread
from typing import List, Optional, Tuple

import cv2
import numpy as np
import torch

from config.video_config import DisplayConfig
from video.video_detector import YOLODetector
from video.video_display import VideoDisplay
from video.windows_control import Windows
from video.fps_tracker import FPSTracker

from logs.logging_setup import setup_logger

################################################################

class Webcam:
    def __init__(self, tts: Queue) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

        self.cap: cv2.VideoCapture = self.load_webcam()
        self.windows: Windows = Windows(self.cap)
        self.device: torch.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model: YOLODetector = YOLODetector(DisplayConfig.WEIGHTS_LOCATION, DisplayConfig.CONFIDENCE_THRESHOLD)
        self.fps_tracker = FPSTracker()

        self.screen_res = self.windows.get_screen_res()
        self.webcam_to_screen_ratio = self.windows.get_webcam_to_screen_ratio(self.screen_res, self.windows.get_camera_res())
        self.last_click_time: float = 0.0
        self.frame: Optional[np.ndarray] = None

        self.frame_lock = Lock()
        self.camera_thread_running = True
        self.camera_thread = Thread(target=self.update_frame, daemon=True)
        self.camera_thread.start()

        self.tts: Queue = tts
        self.tts.put("Camera is initialized!")

    @staticmethod
    def load_webcam() -> cv2.VideoCapture:
        for i in range(0, 5):
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                break
            else:
                time.sleep(0.001)
        if not cap.isOpened():
            raise RuntimeError("Webcam not found.")
        return cap

    def update_frame(self):
        while self.camera_thread_running:
            ret, frame = self.cap.read()
            if ret:
                with self.frame_lock:
                    self.frame = frame

    def perform_inference(self, frame: np.ndarray) -> Tuple[List[int], List[float], List[int]]:
        frame = self.transform_frame(frame)
        return self.model.detect(frame)

    def transform_frame(self, frame: np.ndarray) -> np.ndarray:
        if DisplayConfig.ROTATE_IMAGE:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if DisplayConfig.FLIP_IMAGE_HORIZONTALLY:
            frame = cv2.flip(frame, 1)
        if DisplayConfig.FLIP_IMAGE_VERTICALLY:
            frame = cv2.flip(frame, 0)

        return frame

    def most_confident_box(self, boxes: List[List[int]], confidences: List[float], class_ids: List[int]) -> Tuple[List[int], int]:
        if len(confidences) == 0:
            return None, None

        max_index = np.argmax(confidences)
        box = boxes[max_index]
        label = class_ids[max_index]

        return box, label

    def find_box_center(self, box: List[int]) -> Tuple[int, int]:
        x0, y0, x1, y1 = box
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2

        x = max(0, min(int(x * self.webcam_to_screen_ratio[0]), self.screen_res[0] - 1))
        y = max(0, min(int(y * self.webcam_to_screen_ratio[1]), self.screen_res[1] - 1))

        return x, y

    def process_video(self) -> None:
        attempts: int = 0
        while self.frame is None and attempts < DisplayConfig.MAX_CAMERA_LOAD_ATTEMPTS:
            time.sleep(0.01)
            attempts += 1

        try:
            while True:
                with self.frame_lock:
                    frame = self.frame.copy() if self.frame is not None else None

                if frame is None:
                    self.logger.warning("No frame received from webcam.")
                    break

                boxes, confidences, class_ids = self.perform_inference(frame)
                box, label = self.most_confident_box(boxes, confidences, class_ids)

                if box is not None:
                    self.perform_action(box, label)
                
                self.fps_tracker.update()

                if DisplayConfig.GUI_ENABLED:
                    if box is not None:
                        frame = VideoDisplay.annotate_frame(frame, box, label)

                    VideoDisplay.insert_text_onto_frame(frame, f'FPS: {int(self.fps_tracker.displayed_fps)}', row=1)
                    VideoDisplay.show_frame("GAIA Test", frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            self.camera_thread_running = False
            self.camera_thread.join()
            self.cap.release()
            if DisplayConfig.GUI_ENABLED:
                cv2.destroyAllWindows()

    def perform_action(self, box: List[int], class_id: int) -> None:
        label: str = DisplayConfig.LABELS[class_id]
        x, y = self.find_box_center(box)

        if label == 'hand_open':
            self.windows.unclick()
            start_x, start_y = self.windows.get_cursor_pos()
            self.windows.move_mouse(start_x, start_y, x, y)
            return

        elif label == 'hand_closed':
            self.windows.unclick()
            return

        elif label == 'hand_pinching':
            self.windows.clicking = True
            self.windows.move_mouse(*self.windows.get_cursor_pos(), x, y)
            if time.time() - self.last_click_time >= DisplayConfig.CLICK_DELAY:
                self.windows.left_mouse_down()
                self.last_click_time = time.time()
            return

        elif label == 'thumbs_up':
            self.windows.unclick()
            self.windows.mouse_scroll('up')
            return

        elif label == 'thumbs_down':
            self.windows.unclick()
            self.windows.mouse_scroll('down')
            return

##############################################################################################


if __name__ == '__main__':
    cam = Webcam()
    try:
        cam.process_video()
    except KeyboardInterrupt:
        cam.logger.info("Interrupted by user.")