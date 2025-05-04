from constants.language_config import LanguageConfig
from logs.logging_setup import setup_logger
from apis.router import CommandRouter
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizerFast, BertForTokenClassification
import torch.nn.functional as F
import torch
import os
import logging
from queue import Queue
from pathlib import Path
from typing import Dict, List, Tuple
logging.getLogger(
    "torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.FATAL)


################################################################


class TextToAction:
    def __init__(self, tts_queue: Queue) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.tts_queue = tts_queue
        self.classifer_model_path = Path(
            "language/classifier/weights").resolve()
        self.ner_model_root = Path("language/ner/weights").resolve()
        self.initialize_models_and_tokenizers()
        self.command_router = CommandRouter(self.tts_queue)

    def initialize_models_and_tokenizers(self) -> None:
        self.ner_models = {}
        self.ner_tokenizers = {}
        try:
            for subdir in self.ner_model_root.iterdir():
                if subdir.is_dir():
                    label = subdir.name
                    model = BertForTokenClassification.from_pretrained(
                        subdir, local_files_only=True).eval()
                    tokenizer = BertTokenizerFast.from_pretrained(
                        subdir, local_files_only=True)
                    self.ner_models[label] = (model, tokenizer)

            self.classifier_model = AutoModelForSequenceClassification.from_pretrained(
                self.classifer_model_path, local_files_only=True).eval()
            self.classifier_tokenizer = AutoTokenizer.from_pretrained(
                self.classifer_model_path, local_files_only=True)
        except Exception as e:
            self.logger.error(f"Model init error: {e}")

    def predict_classes(self, text: str) -> Tuple[str, float]:
        inputs = self.classifier_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            logits = self.classifier_model(**inputs).logits
            probs = F.softmax(logits, dim=1)

        index = torch.argmax(probs, dim=1).item()
        label = LanguageConfig.CLASS_NAMES[index]
        confidence = probs[0][index].item()

        return label, confidence

    def predict_entities(self, label: str, text: str) -> List:
        if label not in self.ner_models:
            self.logger.warning(f"No NER model found for label '{label}'")
            return []

        model, tokenizer = self.ner_models[label]

        inputs = tokenizer(text, return_tensors="pt",
                           truncation=True, padding=True)

        with torch.no_grad():
            logits = model(**inputs).logits

        predicted_ids = torch.argmax(logits, dim=-1)[0]
        input_ids = inputs["input_ids"][0]
        tokens = tokenizer.convert_ids_to_tokens(
            input_ids, skip_special_tokens=True)
        labels = [model.config.id2label[idx.item()]
                  for idx in predicted_ids[1:-1]]

        entities = {}
        current_label = None
        current_tokens = []

        for token, label in zip(tokens, labels):
            if label == "O":
                if current_label and current_tokens:
                    phrase = tokenizer.convert_tokens_to_string(
                        current_tokens).replace(" ##", "")
                    entities.setdefault(
                        current_label, []).append(phrase.strip())
                    current_label = None
                    current_tokens = []
                continue

            if label.startswith("B-"):
                if current_label and current_tokens:
                    phrase = tokenizer.convert_tokens_to_string(
                        current_tokens).replace(" ##", "")
                    entities.setdefault(
                        current_label, []).append(phrase.strip())
                current_label = label[2:]
                current_tokens = [token]
            elif label.startswith("I-") and current_label == label[2:]:
                current_tokens.append(token)
            else:
                if current_label and current_tokens:
                    phrase = tokenizer.convert_tokens_to_string(
                        current_tokens).replace(" ##", "")
                    entities.setdefault(
                        current_label, []).append(phrase.strip())
                current_label = None
                current_tokens = []

        if current_label and current_tokens:
            phrase = tokenizer.convert_tokens_to_string(
                current_tokens).replace(" ##", "")
            entities.setdefault(current_label, []).append(phrase.strip())

        return entities

    def clean_entities(self, raw_elements: Dict[str, list]) -> Dict[str, str]:
        return {
            key.lower(): "".join(val).replace("##", "").strip().lower()
            for key, val in raw_elements.items()
        }

    def process_text(self, text: str) -> None:
        success = False
        label = ""
        confidence = 0.0
        for _ in range(3):
            label, confidence = self.predict_classes(text)
            if confidence >= LanguageConfig.COMMAND_CONFIDENCE_THRESHOLD:
                success = True
                break

        if not success:
            self.tts_queue.put("I don't support that feature. Try again.")
            return None

        elements = self.predict_entities(label, text)
        if not elements:
            self.logger.warning(
                "No valid entities were recognized in the command.")
            return None

        elements = self.clean_entities(elements)

        try:

            self.command_router.route(label, elements)
        except Exception as e:
            self.logger.error(f"Error while processing command: {str(e)}")
            return None

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
