import os
import logging
from queue import Queue
logging.getLogger(
    "torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.FATAL)

from apis.router import CommandRouter
from language.classifier_manager import load_classifier_model, predict_classes
from language.ner_manager import load_ner_models, predict_entities
from logs.logging_setup import setup_logger
from constants.language_config import LanguageConfig


################################################################

class TextToAction:
    def __init__(self, tts_queue: Queue) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.tts_queue = tts_queue
        self.ner_models = {}
        self.classifier_model = None
        self.classifier_tokenizer = None
        self.command_router = CommandRouter(self.tts_queue)

        self.load_models()

    def load_models(self) -> None:
        try:
            self.ner_models = load_ner_models()
            self.classifier_model, self.classifier_tokenizer = load_classifier_model()
        except Exception as e:
            self.logger.error(f"Model initialization failed: {e}")

    def process_text(self, text: str) -> None:
        label, confidence = predict_classes(text, self.classifier_model, self.classifier_tokenizer)

        if confidence <= LanguageConfig.COMMAND_CONFIDENCE_THRESHOLD:
            self.tts_queue.put("I don't support that feature. Try again.")
            return None

        entities = predict_entities(label, text, self.ner_models, self.logger)

        if not entities:
            self.logger.warning("No valid entities were recognized in the command.")
            return

        try:
            self.command_router.route(label, entities)
        except Exception as e:
            self.logger.error(f"Command processing error: {str(e)}")

################################################################

def main():
    tts_queue = Queue()
    tta = TextToAction(tts_queue)

    while True:
        try:
            command = input("Enter a command: ")
            tta.process_text(command)
        except Exception as e:
            print(f'An Error Occurred with Action Management: {str(e)}')

################################################################

if __name__ == "__main__":
    main()
