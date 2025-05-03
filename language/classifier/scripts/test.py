from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config.command_config import CommandConfig

#############################################################

class Tester:
    def __init__(self):
        self.model_path = Path("language/ner/weights/music").resolve()
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()
    
    def load_model(self):
        return AutoModelForSequenceClassification.from_pretrained(self.model_path).eval()

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_path)
    
    def predict_classes(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = F.softmax(logits, dim=1)

        index = torch.argmax(probs, dim=1).item()
        label = CommandConfig.CLASS_NAMES[index]
        confidence = probs[0][index].item()

        return label, confidence

#############################################################

def main():
    tester = Tester()

    print("Type a sentence and the model will classify it (type 'exit' to stop):")

    while True:
        sentence = input(">> ").strip().lower()
        if sentence == "exit":
            print("Exiting")
            break

        label, confidence = tester.predict_classes(sentence)

        print(f"Label: {label} (Confidence: {confidence:.2%})\n")

#############################################################

if __name__ == "__main__":
    main()