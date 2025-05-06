import logging
from typing import Tuple
from pathlib import Path
logging.getLogger(
    "torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.ERROR)

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from constants.language_config import LanguageConfig

#############################################################


class ModelTester:
    def __init__(self) -> None:
        self.model_path = Path("language/classifier/weights").resolve()
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()

    def load_model(self) -> AutoModelForSequenceClassification:
        return AutoModelForSequenceClassification.from_pretrained(self.model_path).eval()

    def load_tokenizer(self) -> AutoTokenizer:
        return AutoTokenizer.from_pretrained(self.model_path)

    def predict_classes(self, text: str) -> Tuple[str, float]:
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = F.softmax(logits, dim=1)

        index = torch.argmax(probs, dim=1).item()
        label = LanguageConfig.CLASS_NAMES[index]
        confidence = probs[0][index].item()

        return label, confidence

#############################################################


def main() -> None:
    tester = ModelTester()

    print("Type a sentence and the model will classify it (type 'exit' to stop):")

    while True:
        text = input(">> ").strip().lower()
        if text == "exit":
            print("Exiting")
            break

        label, confidence = tester.predict_classes(text)

        print(f"Label: {label} (Confidence: {confidence:.2%})\n")

#############################################################


if __name__ == "__main__":
    main()
