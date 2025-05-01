import torch

class PathConfig:
    BERT_WEIGHTS_LOCATION = "results\\checkpoint-120"

    if torch.cuda.is_available():
        YOLO_WEIGHTS_LOCATION: str = "video\\train\\weights\\best.engine"
    else:
        YOLO_WEIGHTS_LOCATION: str = "video\\train\\weights\\best.onnx"