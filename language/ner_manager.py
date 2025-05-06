from pathlib import Path
from typing import Dict, Tuple

import torch
from transformers import BertTokenizerFast, BertForTokenClassification

#############################################################

def load_ner_models() -> Dict[str, Tuple[BertForTokenClassification, BertTokenizerFast]]:
    root = Path("language/ner/weights").resolve()
    models = {}
    for subdir in root.iterdir():
        if subdir.is_dir():
            label = subdir.name
            model = BertForTokenClassification.from_pretrained(subdir, local_files_only=True).eval()
            tokenizer = BertTokenizerFast.from_pretrained(subdir, local_files_only=True)
            models[label] = (model, tokenizer)
    return models

def predict_entities(label: str, text: str, ner_models: Dict[str, Tuple[BertForTokenClassification, BertTokenizerFast]], logger) -> Dict[str, str]:
    if label not in ner_models:
        logger.warning(f"No NER model found for label '{label}'")
        return {}

    model, tokenizer = ner_models[label]
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_ids = torch.argmax(logits, dim=-1)[0]
    input_ids = inputs["input_ids"][0]
    tokens = tokenizer.convert_ids_to_tokens(input_ids, skip_special_tokens=True)
    labels = [model.config.id2label[idx.item()] for idx in predicted_ids[1:-1]]

    entities = {}
    current_label = None
    current_tokens = []

    for token, label in zip(tokens, labels):
        if label == "O":
            if current_label and current_tokens:
                _add_entity(entities, current_label, tokenizer, current_tokens)
            current_label, current_tokens = None, []
            continue

        if label.startswith("B-"):
            if current_label and current_tokens:
                _add_entity(entities, current_label, tokenizer, current_tokens)
            current_label = label[2:]
            current_tokens = [token]
        elif label.startswith("I-") and current_label == label[2:]:
            current_tokens.append(token)
        else:
            if current_label and current_tokens:
                _add_entity(entities, current_label, tokenizer, current_tokens)
            current_label, current_tokens = None, []

    if current_label and current_tokens:
        _add_entity(entities, current_label, tokenizer, current_tokens)

    if entities:
        entities = clean_entities(entities)

    return entities

def _add_entity(entities: Dict[str, list], label: str, tokenizer: BertTokenizerFast, tokens: list) -> None:
    phrase = tokenizer.convert_tokens_to_string(tokens).replace(" ##", "").strip()
    entities.setdefault(label, []).append(phrase)

def clean_entities(raw_elements: Dict[str, list]) -> Dict[str, str]:
    return {
        key.lower(): "".join(val).replace("##", "").strip().lower()
        for key, val in raw_elements.items()
    }