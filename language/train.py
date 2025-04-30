import os
import shutil
import pandas as pd

import torch
import evaluate
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizerFast, BertForSequenceClassification, TrainingArguments, Trainer

class GenerateModel():
    def __init__(self):
        self.clean_workspace()
        self.tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
        self.model = self.load_model()
        self.train_dataset, self.val_dataset = self.get_dataset()

    def clean_workspace(self):
        if os.path.exists("./results"):
            shutil.rmtree("./results")

    def load_model(self):
        model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=17)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Model running on {device}")
        model = model.to(device)

        return model

    def get_dataset(self):
        train_df = pd.read_csv("data/train.csv")
        val_df = pd.read_csv("data/val.csv")

        label_encoder = LabelEncoder()
        label_encoder.fit(train_df['label'])

        train_df['label'] = label_encoder.transform(train_df['label']).astype(int)
        val_df['label'] = label_encoder.transform(val_df['label']).astype(int)

        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)

        train_dataset = train_dataset.map(self.tokenize, batched=True)
        val_dataset = val_dataset.map(self.tokenize, batched=True)

        train_dataset = train_dataset.remove_columns(["text"])
        val_dataset = val_dataset.remove_columns(["text"])

        train_dataset.set_format("torch")
        val_dataset.set_format("torch")

        return train_dataset, val_dataset

    def tokenize(self, batch):
        return self.tokenizer(batch['text'], padding='max_length', truncation=True, max_length=128)

    def compute_metrics(self, eval_pred):
        logits, labels = eval_pred
        preds = torch.argmax(torch.tensor(logits), dim=1)
        accuracy = evaluate.load("accuracy")
        return accuracy.compute(predictions=preds, references=torch.tensor(labels))
    
    def train(self):
        training_args = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=50,
            per_device_eval_batch_size=50,
            num_train_epochs=3,
            weight_decay=0.01,
            logging_dir="./logs",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset,
            tokenizer=self.tokenizer,
            compute_metrics=self.compute_metrics,
        )
        
        trainer.train()

if __name__ == "__main__":
    model = GenerateModel()
    model.train()