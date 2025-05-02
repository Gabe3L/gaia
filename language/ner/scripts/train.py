import os
import shutil
from pathlib import Path

import torch
import pandas as pd
from simpletransformers.ner import NERModel, NERArgs

#############################################################

TASK = "music"

#############################################################

class PathConfig:
    NER_PATH = Path("language/ner")
    TRAIN_DATASET = Path(NER_PATH / "data" / TASK / "train.csv")
    VAL_DATASET = Path(NER_PATH / "data" / TASK / "val.csv")
    BEST_MODEL_DIR = Path(NER_PATH / "weights" / TASK)
    OUTPUT_DIR = Path(NER_PATH / "results")
    CACHE_DIR = Path(NER_PATH / "cache")

class GenerateModel:
    def __init__(self):
        self.train_dataset = pd.read_csv(PathConfig.TRAIN_DATASET)
        self.val_dataset = pd.read_csv(PathConfig.VAL_DATASET)
        self.model = self.load_model()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def clear_cache(self):
        if os.path.exists(PathConfig.CACHE_DIR):
            shutil.rmtree(PathConfig.CACHE_DIR)
    
    def clear_poor_results(self):
        if os.path.exists(PathConfig.OUTPUT_DIR):
            shutil.rmtree(PathConfig.OUTPUT_DIR)

    def load_model(self) -> NERModel:
        model_args = NERArgs()
        model_args.overwrite_output_dir = True
        model_args.reprocess_input_data = True
        model_args.evaluate_during_training = True
        model_args.evaluate_during_training_steps = 200
        model_args.save_best_model = True
        model_args.num_train_epochs = 5
        model_args.train_batch_size = 16
        model_args.eval_batch_size = 16
        model_args.save_steps = 200
        model_args.max_seq_length = 128
        model_args.learning_rate = 3e-5
        model_args.output_dir = PathConfig.OUTPUT_DIR
        model_args.best_model_dir = PathConfig.BEST_MODEL_DIR
        model_args.cache_dir = PathConfig.CACHE_DIR
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
        self.model.train_model(
            train_data=self.train_dataset,
            eval_data=self.val_dataset
        )
        result, model_outputs, predictions = self.model.eval_model(self.val_dataset)
        print(result)
        
#############################################################

if __name__ == "__main__":
    model = GenerateModel()
    model.train()
    model.clear_poor_results()
    model.clear_cache()