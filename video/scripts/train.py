import os
import json
import shutil
import logging

import roboflow
from ultralytics import YOLO

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def get_config():
    logger.info("Loading Config.")

    with open("admin/roboflow_creds.json", "r") as f:
        config = json.load(f)

    return config

def get_roboflow_workspace(config):
    logger.info("Accessing Roboflow")
    rf = roboflow.Roboflow()
    return rf.workspace(config["workspace"]).project(config["project"]).version(config["version"])

def get_dataset(config, project):
    logger.info("Downloading Dataset")

    return project.download(
        config["model_type"], 
        location="video_ai/datasets"
    )

def delete_dataset(dataset):
    dataset_path = dataset.location
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)
        logger.info(f"Dataset at '{dataset_path}' deleted.")
    else:
        logger.warning(f"Dataset path '{dataset_path}' not found.")

def train(dataset):
    try:
        logger.info("Beginning Training.")
        model = YOLO("video_ai/yolo11n.pt").to("cuda")
        model.train(
            data=os.path.join(dataset.location, "data.yaml"),
            project="video_ai",
            device="cuda",
            batch=60,
            imgsz=640,
            epochs=100,
            workers=8,
            nms=True,
            iou=0.6,
            amp=True,
            half=True
        )

        logger.info("Exporting model...")
        model.export(format="onnx", half=True, device="cuda")
        model.export(format="engine", half=True, device="cuda")
    except Exception as e:
        logger.error(e)

def main():
    roboflow.login()

    config = get_config()
    workspace = get_roboflow_workspace(config)
    dataset = get_dataset(config, workspace)
    train(dataset)
    delete_dataset(dataset)

#################################################################################################

if __name__ == "__main__":
    main()
