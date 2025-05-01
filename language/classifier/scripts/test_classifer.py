import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

from config.command_config import CommandConfig

model_dir = "results/checkpoint-120"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model.eval()

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
    pred_label = CommandConfig.CLASS_NAMES[pred_idx]
    confidence = probs[0][pred_idx].item()

    print(f"Prediction: {pred_label} (Confidence: {confidence:.2%})\n")
