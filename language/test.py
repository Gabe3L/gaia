import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

model_dir = "results/checkpoint-120"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model.eval()

class_names = [
    "greeting", "date", "time", "weather", "music", "joke", 
    "news", "note", "location", "wiki", "calendar", "system", 
    "shutdown", "website", "launch", "google", "youtube"
]

print("Type a sentence and I'll classify it. Type 'exit' to quit.\n")

while True:
    sentence = input(">> ").lower()
    if sentence == "exit":
        break

    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=1)

    pred_idx = torch.argmax(probs, dim=1).item()
    pred_label = class_names[pred_idx]
    confidence = probs[0][pred_idx].item()

    print(f"Prediction: {pred_label} (Confidence: {confidence:.2%})\n")
