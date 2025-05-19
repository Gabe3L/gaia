import cv2
import math
import ctypes
from typing import Tuple

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]


class Windows:
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_WHEEL = 0x0800

    def __init__(self) -> None:
        self.clicking = False
        self.mci = ctypes.WinDLL('winmm')
        self.user32 = ctypes.windll.user32

    def get_cursor_pos(self) -> Tuple[int, int]:
        point = POINT()
        self.user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y

    def get_screen_res(self) -> Tuple[int, int]:
        return (self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1))

    def get_webcam_to_screen_ratio(self, screen_res: int, camera_res: int) -> Tuple[float, float]:
        return (screen_res[0] / screen_res[1], camera_res[0] / camera_res[1])

    def mouse_event(self, dwFlags: int, dx: int = 0, dy: int = 0, dwData: int = 0, dwExtraInfo: int = 0) -> None:
        self.user32.mouse_event(dwFlags, dx, dy, dwData, dwExtraInfo)

    def left_mouse_down(self) -> None:
        self.mouse_event(self.MOUSEEVENTF_LEFTDOWN)

    def left_mouse_up(self) -> None:
        self.mouse_event(self.MOUSEEVENTF_LEFTUP)

    def move_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        dx = end_x - start_x
        dy = end_y - start_y
        steps = max(int(math.hypot(dx, dy)), 1)
        step_x = dx / steps
        step_y = dy / steps

        for i in range(steps):
            x = int(start_x + step_x * i)
            y = int(start_y + step_y * i)
            self.user32.SetCursorPos(int(x), int(y))
        self.user32.SetCursorPos(int(end_x), int(end_y))

    def mouse_scroll(self, direction: str) -> None:
        directions = {'up': 100, 'down': -100}
        self.mouse_event(self.MOUSEEVENTF_WHEEL, dwData=directions[direction])

    def unclick(self) -> None:
        if self.clicking:
            self.left_mouse_up()
            self.clicking = False