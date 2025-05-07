import os
import traceback
from typing import Optional
from queue import Queue, Empty
from threading import Thread, Event
from backend.logs.logging_setup import setup_logger

from backend.app.video.video_ai import Webcam
from backend.app.audio.speech_to_text import SpeechToText
from backend.app.audio.text_to_speech import TextToSpeech
from backend.app.language.text_to_action import TextToAction

################################################################


class Gaia():
    def __init__(self):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

    def handle_performing_actions(self, stop_event, speech_queue: Queue, command_queue: Queue) -> None:
        tta = TextToAction(speech_queue)

        while not stop_event.is_set():
            try:
                request = command_queue.get(timeout=0.5)
                if request:
                    tta.process_text(request)
            except Empty:
                continue
            except Exception as e:
                self.logger.error(
                    f'An Error Occurred with Action Management: {type(e).__name__} - {str(e)}\n{traceback.format_exc()}')

    def handle_speech_to_text(self, stop_event, speech_queue: Queue, command_queue: Queue) -> None:
        stt = SpeechToText(speech_queue)
        while not stop_event.is_set():
            try:
                request = stt.process_audio()
                if request:
                    self.logger.info(f'Computer Understood: {request}')
                    command_queue.put(request)
            except Exception as e:
                self.logger.error(
                    f'An Error Occurred with Audio Processing: {str(e)}')

    def handle_camera(self, stop_event, speech_queue: Queue) -> None:
        camera = Webcam(speech_queue)

        while not stop_event.is_set():
            try:
                camera.process_video()
            except Exception as e:
                self.logger.error(
                    f'An Error Occurred with Video Processing: {str(e)}')

    def handle_text_to_speech(self, stop_event, speech_queue: Queue) -> None:
        tts = TextToSpeech()
        while not stop_event.is_set():
            try:
                request: Optional[str] = speech_queue.get(timeout=0.5)
                if request:
                    tts.speak(request)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(
                    f'An Error Occurred with Audio Processing: {str(e)}')


class ThreadManager():
    def __init__(self, gaia: Gaia):
        self.logger = gaia.logger
        self.gaia = gaia
        self.threads: list[Thread] = []

    def start_all_threads(self, stop_event: Event, speech_queue: Queue, command_queue: Queue) -> None:
        try:
            self.threads = [
                Thread(target=self.gaia.handle_performing_actions,
                       args=(stop_event, speech_queue, command_queue)),
                Thread(target=self.gaia.handle_speech_to_text, args=(
                    stop_event, speech_queue, command_queue)),
                Thread(target=self.gaia.handle_text_to_speech,
                       args=(stop_event, speech_queue)),
                Thread(target=self.gaia.handle_camera,
                       args=(stop_event, speech_queue))
            ]

            for thread in self.threads:
                thread.start()

            self.logger.info("All threads started successfully.")
        except Exception as e:
            self.logger.error(f'Failed to start threads: {str(e)}')

    def close_all_threads(self):
        for thread in self.threads:
            thread.join()
        self.logger.info("All threads joined and closed.")


def main() -> None:
    stop_event = Event()
    speech_queue = Queue()
    command_queue = Queue()

    gaia = Gaia()
    thread_manager = ThreadManager(gaia)

    try:
        thread_manager.start_all_threads(
            stop_event, speech_queue, command_queue)
        while not stop_event.is_set():
            stop_event.wait(timeout=1)
    except KeyboardInterrupt:
        stop_event.set()
        thread_manager.close_all_threads()

################################################################


if __name__ == '__main__':
    main()
