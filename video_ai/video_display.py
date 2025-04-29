import cv2
import numpy as np
from PIL import Image, ImageDraw
from typing import List, Tuple

from video_ai.video_config import DisplayConfig

class VideoDisplay:
    def __init__(self) -> None:
        pass

    @staticmethod
    def show_frame(window_name: str, frame: np.ndarray) -> None:
        """Displays the frame in a window."""
        cv2.imshow(window_name, frame)

    @staticmethod
    def annotate_frame(frame: np.ndarray, box: Tuple[int, int, int, int], class_id: int) -> np.ndarray:
        """Annotate the frame with bounding boxes and labels."""
        color = DisplayConfig.LABEL_COLOURS.get(class_id, (255, 255, 255))
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)

        return frame
    
    @staticmethod
    def insert_text_onto_frame(frame: np.ndarray, message: List[str], row: int) -> np.ndarray:
        """Annotate the frane with text"""
        if message:
            cv2.putText(frame, message, (10, (30 + (row * 50))), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    
    @staticmethod
    def draw_box(score: float, box: np.ndarray, label: str, colour: tuple[int, int, int], image: Image.Image) -> Image.Image:
        x0, y0, x1, y1 = map(int, box.tolist())
        draw = ImageDraw.Draw(image)
        draw.rectangle([x0, y0, x1, y1], outline=colour, width=3)
        draw.text((10, 10), f'Action: {label}', fill="black")
        draw.text((image.width - 75, 10), f'Score: {(score * 100):.0f}%', fill="black")
        return image