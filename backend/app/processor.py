import os
import traceback
from queue import Queue, Empty
from typing import Optional, Dict
from threading import Thread, Event

from backend.logs.logging_setup import setup_logger
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
        self.threads: Dict[str, Thread] = {}
        self.stop_event: Optional[Event] = None

    def start_all_threads(self, stop_event: Event, speech_queue: Queue, command_queue: Queue):
        self.stop_event = stop_event
        self.start_thread("performing_actions", speech_queue, command_queue)
        self.start_thread("speech_to_text", speech_queue, command_queue)
        self.start_thread("text_to_speech", speech_queue, command_queue)
        self.start_thread("camera", speech_queue, command_queue)

    def close_all_threads(self):
        if self.stop_event:
            self.stop_event.set()
        for thread in self.threads.values():
            thread.join()
        self.threads.clear()
        self.logger.info("All threads stopped.")

    def start_thread(self, name: str, speech_queue: Queue, command_queue: Queue):
        if name in self.threads and self.threads[name].is_alive():
            self.logger.info(f"Thread '{name}' is already running.")
            return

        if self.stop_event is None:
            self.logger.error("Stop event not initialized.")
            return

        match name:
            case "performing_actions":
                thread = Thread(target=self.gaia.handle_performing_actions,
                                args=(self.stop_event, speech_queue, command_queue))
            case "speech_to_text":
                thread = Thread(target=self.gaia.handle_speech_to_text,
                                args=(self.stop_event, speech_queue, command_queue))
            case "text_to_speech":
                thread = Thread(target=self.gaia.handle_text_to_speech,
                                args=(self.stop_event, speech_queue))
            case _:
                self.logger.error(f"No such thread: {name}")
                return

        thread.start()
        self.threads[name] = thread
        self.logger.info(f"Thread '{name}' started.")

    def stop_thread(self, name: str):
        if name in self.threads:
            self.threads[name].join()
            del self.threads[name]
            self.logger.info(f"Thread '{name}' stopped.")
        else:
            self.logger.warning(f"Thread '{name}' is not running.")


################################################################


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
