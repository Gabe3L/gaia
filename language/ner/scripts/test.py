import torch
from transformers import BertTokenizerFast, BertForTokenClassification

model = BertForTokenClassification.from_pretrained(r"C:\Users\Gabe3\Documents\Visual Studio Workspace\gaia\language\ner\results\checkpoint-3-epoch-3")
tokenizer = BertTokenizerFast.from_pretrained(r"C:\Users\Gabe3\Documents\Visual Studio Workspace\gaia\language\ner\results\checkpoint-3-epoch-3")

model.eval()

def predict_entities(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    predicted_ids = torch.argmax(logits, dim=-1)
    
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    predicted_labels = [model.config.id2label[id.item()] for id in predicted_ids[0]]
    
    combined_results = []
    current_word_tokens = []
    current_word_label = None

    for token, label in zip(tokens, predicted_labels):
        if label != 'O':
            if token == '[CLS]' or token == '[SEP]':
                continue
            
            if token.startswith('##'):
                current_word_tokens.append(token[2:])
            else:
                if current_word_tokens:
                    combined_results.append((''.join(current_word_tokens), current_word_label))
                current_word_tokens = [token]
                current_word_label = label
    
    if current_word_tokens:
        combined_results.append((''.join(current_word_tokens), current_word_label))
    
    return combined_results

def interactive_test():
    print("Type your sentence and the model will predict named entities (type 'exit' to stop):")
    
    while True:
        text = input("You: ").lower()
        
        if text == "exit":
            print("Exiting... Goodbye!")
            break
        
        entities = predict_entities(text)
        
        if entities:
            print("\nPredicted entities:")
            for token, label in entities:
                print(f"Token: {token} -> Label: {label}")
        else:
            print("No entities detected.\n")

if __name__ == "__main__":
    interactive_test()
