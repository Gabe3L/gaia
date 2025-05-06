import os
import shutil
import logging
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")
logging.getLogger("torch.distributed.elastic.multiprocessing.redirects").setLevel(logging.ERROR)

import torch
import pandas as pd
from simpletransformers.classification import ClassificationModel, ClassificationArgs

#############################################################

class PathConfig:
    CLASSIFIER = Path("language/classifier")
    TRAIN_DATASET = Path(CLASSIFIER / "data" / "train.csv")
    VAL_DATASET = Path(CLASSIFIER / "data" / "val.csv")
    BEST_MODEL_DIR = Path(CLASSIFIER / "weights")
    OUTPUT_DIR = Path(CLASSIFIER / "results")
    CACHE_DIR = Path(CLASSIFIER / "cache")

class ModelTrainer():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.train_dataset, self.val_dataset = self.get_dataset()
        self.model = self.load_model()

    def clear_cache(self):
        if os.path.exists(PathConfig.CACHE_DIR):
            shutil.rmtree(PathConfig.CACHE_DIR)
    
    def clear_poor_results(self):
        if os.path.exists(PathConfig.OUTPUT_DIR):
            shutil.rmtree(PathConfig.OUTPUT_DIR)

    def get_dataset(self):
        train_dataset = pd.read_csv(PathConfig.TRAIN_DATASET)
        val_dataset = pd.read_csv(PathConfig.VAL_DATASET)

        return train_dataset, val_dataset

    def load_model(self):
        model_args = ClassificationArgs(
            # Logging
            logging_steps=0,

            # Learning
            num_train_epochs = 5,
            learning_rate = 3e-5,
            save_best_model = True,
            evaluate_during_training = True,

            # Resources
            fp16=True,
            use_multiprocessing=False,
            use_multiprocessing_for_evaluation=False,
            train_batch_size = 50,
            eval_batch_size = 50,
            
            # Paths
            overwrite_output_dir=True,
            output_dir=str(PathConfig.OUTPUT_DIR),
            best_model_dir=str(PathConfig.BEST_MODEL_DIR),
            cache_dir=str(PathConfig.CACHE_DIR),
        )

        return ClassificationModel(
            model_type="distilbert",
            model_name="distilbert-base-uncased",
            num_labels=17,
            args=model_args,
            use_cuda=torch.cuda.is_available()
        )

    def train(self):
        self.model.train_model(
            train_df=self.train_dataset, 
            eval_df=self.val_dataset
        )
        result, model_outputs, predictions = self.model.eval_model(self.val_dataset)
        print(result)

#############################################################

def main():
    model = ModelTrainer()
    model.train()
    model.clear_poor_results()
    model.clear_cache()

#############################################################

if __name__ == "__main__":
    main()