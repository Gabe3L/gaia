from pathlib import Path

import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from tabulate import tabulate

#############################################################

class Tester:
    def __init__(self):
        self.model_path = Path("language/ner/weights/music").resolve()
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()

    def load_model(self):
        return BertForTokenClassification.from_pretrained(self.model_path, local_files_only=True).eval()

    def load_tokenizer(self):
        return BertTokenizerFast.from_pretrained(self.model_path, local_files_only=True)

    def predict_entities(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        predicted_ids = torch.argmax(logits, dim=-1)[0]
        input_ids = inputs["input_ids"][0]
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids, skip_special_tokens=True)
        labels = [self.model.config.id2label[idx.item()] for idx in predicted_ids[1:-1]]
        full_text = self.tokenizer.convert_tokens_to_string(tokens).split()
        
        entities = []
        i = 0
        for word in full_text:
            if i < len(labels):
                label = labels[i]
                if label != "O":
                    entities.append((word, label))
                i += 1

        return entities

#############################################################

def main():
    tester = Tester()

    print("Type a sentence and the model will predict entities (type 'exit' to stop):")

    while True:
        text = input("You: ").strip().lower()
        
        while True:
            if text == "exit":
                print("Exiting")
                break
            
            entities = tester.predict_entities(text)
            
            if entities:
                print("\nPredicted entities:")
                print(tabulate(entities, headers=["Token", "Label"], tablefmt="fancy_grid"))
            else:
                print("No entities detected.\n")

#############################################################

if __name__ == "__main__":
    main()