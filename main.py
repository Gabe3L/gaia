aimport os
from typing import Optional
from queue import Queue, Empty
from threading import Thread, Event
from logs.logging_setup import setup_logger

from features.features import ActionManager
from video_ai.video_ai import Webcam
from audio_ai.speech_to_text import SpeechToText
from audio_ai.text_to_speech import TextToSpeech

################################################################


class Gaia():
    def __init__(self):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

    def handle_performing_actions(self, stop_event, tts_queue: Queue, request_queue: Queue) -> None:
        manager = ActionManager(tts_queue, request_queue)
        manager.welcome_user()

        while not stop_event.is_set():
            try:
                manager.execute_task(request_queue.get(), tts_queue)
            except Exception as error_message:
                self.logger.error(
                    f'An Error Occurred with Action Management: {str(error_message)}')

    def handle_speech_to_text(self, stop_event, tts_queue: Queue, request_queue: Queue) -> None:
        stt = SpeechToText(tts_queue)
        while not stop_event.is_set():
            try:
                request = stt.process_audio()
                self.logger.info(f'Computer Understood: {request}')
                request_queue.put(request)
            except Exception as error_message:
                self.logger.error(
                    f'An Error Occurred with Audio Processing: {str(error_message)}')

    def handle_camera(self, stop_event, tts_queue: Queue) -> None:
        camera = Webcam(tts_queue)

        while not stop_event.is_set():
            try:
                camera.process_video()
            except Exception as error_message:
                self.logger.error(
                    f'An Error Occurred with Video Processing: {str(error_message)}')

    def handle_text_to_speech(self, stop_event, tts_queue: Queue) -> None:
        tts = TextToSpeech()
        while not stop_event.is_set():
            try:
                request: Optional[str] = tts_queue.get(timeout=0.5)
                if request:
                    tts.speak(request)
            except Empty:
                pass
            except Exception as error_message:
                self.logger.error(
                    f'An Error Occurred with Audio Processing: {str(error_message)}')


class ThreadManager():
    def __init__(self, gaia: Gaia):
        self.logger = gaia.logger
        self.gaia = gaia
        self.threads: list[Thread] = []

    def start_all_threads(self, stop_event: Event, tts_queue: Queue, request_queue: Queue) -> None:
        try:
            self.threads = [
                Thread(target=self.gaia.handle_performing_actions, args=(stop_event, tts_queue, request_queue)),
                Thread(target=self.gaia.handle_speech_to_text, args=(stop_event, tts_queue, request_queue)),
                Thread(target=self.gaia.handle_text_to_speech, args=(stop_event, tts_queue)),
                Thread(target=self.gaia.handle_camera, args=(stop_event, tts_queue))
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
    tts_queue = Queue()
    request_queue = Queue()

    gaia = Gaia()
    thread_manager = ThreadManager(gaia)

    try:
        thread_manager.start_all_threads(stop_event, tts_queue, request_queue)
        while not stop_event.is_set():
            stop_event.wait(timeout=1)
    except KeyboardInterrupt:
        stop_event.set()
        thread_manager.close_all_threads()

################################################################


if __name__ == '__main__':
    main()
