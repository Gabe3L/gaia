from constants.language_config import LanguageConfig
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import torch
import logging
from pathlib import Path
logging.getLogger(
    "torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.ERROR)


#############################################################


class Tester:
    def __init__(self):
        self.model_path = Path("language/classifier/weights").resolve()
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()

    def load_model(self):
        return AutoModelForSequenceClassification.from_pretrained(self.model_path).eval()

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_path)

    def predict_classes(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=128)

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = F.softmax(logits, dim=1)

        index = torch.argmax(probs, dim=1).item()
        label = LanguageConfig.CLASS_NAMES[index]
        confidence = probs[0][index].item()

        return label, confidence

#############################################################


def main():
    tester = Tester()

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
