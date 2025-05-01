import os
from typing import Optional

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from logs.logging_setup import setup_logger
from config.path_config import PathConfig
from config.command_config import CommandConfig

################################################################

class TextToAction:
    def __init__(self, speech_queue):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.model = self.load_model()
        self.tokenizer = AutoTokenizer.from_pretrained(PathConfig.BERT_WEIGHTS_LOCATION)
        self.tts_queue = speech_queue

    def load_model(self):
        model = AutoModelForSequenceClassification.from_pretrained(PathConfig.BERT_WEIGHTS_LOCATION)
        model.eval()
        return model

    def classify_text(self, text: str) -> Optional[str]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = F.softmax(logits, dim=1)

        pred_idx = torch.argmax(probs, dim=1).item()
        pred_label = CommandConfig.CLASS_NAMES[pred_idx]
        confidence = probs[0][pred_idx].item()

        if confidence >= CommandConfig.COMMAND_CONFIDENCE_THRESHOLD:
            return pred_label
        return None