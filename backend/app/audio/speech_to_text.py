import os
import time
import torch
import whisper
import numpy as np
from queue import Queue

from logs.logging_setup import setup_logger
from speech_recognition import Recognizer, Microphone, UnknownValueError

################################################################

class SpeechToText():
    def __init__(self, speech_queue: Queue) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

        self.recording = Recognizer()
        self.tts = speech_queue

        device = "cuda" if torch.cuda.is_available() else "cpu"

        time.sleep(5) #TODO: Find a better fix for GPU Memory

        self.model = whisper.load_model("base").to(device)

    def process_audio(self) -> str:
        try:
            request = self.get_request()
            if request:
                self.logger.info(f"Whisper Heard: {request}")
                return request
        except UnknownValueError:
            self.logger.error("Audio could not be understood.")
        except Exception as e:
            self.logger.error(f"Error in processing audio: {e}")
        
        return None

    def get_request(self) -> str:
        try:
            audio_data = self.capture_audio()
            if audio_data is not None:
                result = self.transcribe_audio(audio_data)
                if result:
                    return result
        except Exception as e:
            self.logger.error(f"Error while getting request: {e}")
        
        return None

    def capture_audio(self) -> np.ndarray:
        try:
            with Microphone(sample_rate=16000) as mic:
                self.recording.adjust_for_ambient_noise(mic, duration=0.5)
                audio = self.recording.listen(mic)

            audio_data = np.frombuffer(audio.get_wav_data(), dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            return audio_data
        except Exception as e:
            self.logger.error(f"Error capturing audio: {e}")
            return None

    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        try:
            result = self.model.transcribe(audio_data)
            text = result["text"].lower()
            
            if text.strip():
                return self.clean_transcription(text)
            else:
                self.logger.warning("Empty transcription result.")
                return None
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            return None
        
    def clean_transcription(self, text: str) -> str:
        unwanted_words = ["um", "uh", "urm"]
        for word in unwanted_words:
            text = text.replace(word, "")
        return text.strip()

################################################################

if __name__ == "__main__":
    speech_queue = Queue()
    stt = SpeechToText(speech_queue)
    while True:
        print(stt.process_audio())