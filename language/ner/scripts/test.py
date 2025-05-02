import torch
from pathlib import Path
from transformers import BertTokenizerFast, BertForTokenClassification
from tabulate import tabulate

model_path = Path("language/ner/results/checkpoint-95-epoch-5").resolve()

model = BertForTokenClassification.from_pretrained(model_path, local_files_only=True)
tokenizer = BertTokenizerFast.from_pretrained(model_path, local_files_only=True)

model.eval()

def predict_entities(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_ids = torch.argmax(logits, dim=-1)[0]
    input_ids = inputs["input_ids"][0]
    tokens = tokenizer.convert_ids_to_tokens(input_ids, skip_special_tokens=True)
    labels = [model.config.id2label[idx.item()] for idx in predicted_ids[1:-1]]
    full_text = tokenizer.convert_tokens_to_string(tokens).split()
    
    entities = []
    i = 0
    for word in full_text:
        if i < len(labels):
            label = labels[i]
            if label != "O":
                entities.append((word, label))
            i += 1

    return entities

def interactive_test():
    print("Type your sentence and the model will predict named entities (type 'exit' to stop):")

    while True:
        text = input("You: ").strip()
        
        if text.lower() == "exit":
            print("Exiting... Goodbye!")
            break
        
        entities = predict_entities(text)
        
        if entities:
            print("\nPredicted entities:")
            print(tabulate(entities, headers=["Token", "Label"], tablefmt="fancy_grid"))
        else:
            print("No entities detected.\n")

if __name__ == "__main__":
    interactive_test()
