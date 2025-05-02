import os
import shutil

import torch
import pandas as pd
from simpletransformers.ner import NERModel, NERArgs

class GenerateModel:
    def __init__(self):
        self.clean_workspace()
        self.train_dataset = pd.read_csv("language/ner/data/music.csv")
        self.model = self.load_model()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def clean_workspace(self):
        if os.path.exists("language/ner/results"):
            shutil.rmtree("language/ner/results")
        if os.path.exists("language/ner/cache"):
            shutil.rmtree("language/ner/cache")

    def load_model(self) -> NERModel:
        model_args = NERArgs()
        model_args.overwrite_output_dir = True
        model_args.reprocess_input_data = True
        model_args.num_train_epochs = 5
        model_args.train_batch_size = 16
        model_args.eval_batch_size = 16
        model_args.save_steps = 200
        model_args.max_seq_length = 128
        model_args.learning_rate = 3e-5
        model_args.output_dir = "language/ner/results/"
        model_args.best_model_dir = "language/ner/results/best_model/"
        model_args.cache_dir = "language/ner/cache"
        model_args.labels_list = [
            'O', 
            'B-ARTIST', 'I-ARTIST', 
            'B-SONG', 'I-SONG', 
            'B-APP', 'I-APP', 
            'B-ALBUM', 'I-ALBUM', 
            'B-GENRE', 'I-GENRE'
        ]


        return NERModel(
            "bert",
            "bert-base-cased",
            args=model_args,
            use_cuda=torch.cuda.is_available()
        )

    def train(self):
        self.model.train_model(train_data=self.train_dataset)
        result, model_outputs, predictions = self.model.eval_model(self.train_dataset)
        print(result)

if __name__ == "__main__":
    model = GenerateModel()
    model.train()