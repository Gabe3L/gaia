import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from constants.language_config import LanguageConfig
from pathlib import Path

def load_classifier_model():
    path = Path("language/classifier/weights").resolve()
    model = AutoModelForSequenceClassification.from_pretrained(path, local_files_only=True).eval()
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    return model, tokenizer

def predict_classes(text: str, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=1)
    index = torch.argmax(probs, dim=1).item()
    label = LanguageConfig.CLASS_NAMES[index]
    confidence = probs[0][index].item()
    return label, confidence