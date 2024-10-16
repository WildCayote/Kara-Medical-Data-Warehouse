import torch, cv2
import pandas as pd
from tqdm import tqdm

def detect_objects(folder_path: str, model: object):
    """
    A function that will detect objects in images found in a directory.

    Args:
        folder_path(str): the path to the directory which contains the images to be detected
        model(object): the YOLO model, this function expectes to be provided one
    
    Returns:
        detection_data(pd.DataFrame): a dataframe containing the bounding box and label of the images
    """
    # a list for containing the detection information
    detections = []

    # get the list of images
    image_files = os.listdir(folder_path)

    # loop throught the images and detect objects
    for path in tqdm(image_files, desc="Processing Images", unit="Images"):
        # load the image using opencv
        image_path = os.path.join(images_folder, path)
        image = cv2.imread(filename=image_path)
        
        # detect objects in the image
        detection_results = model(image)

        for object in detection_results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = object[:6]
            detections.append({
                'image': image_path,
                'class': int(cls),
                'confidence': conf,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2
            })
    
    # convert the list of dicts into a dataframe
    detections = pd.DataFrame(data=detections)

    return detections

def push_detections(table_name: str):
    """"""



if __name__ == "__main__":
    import argparse, os, warnings

    # disable warning
    warnings.simplefilter(action='ignore')

    # define argument for providing the path to images folder and path to export detections to
    parser = argparse.ArgumentParser(
        prog="Object Detector",
        description="A script that "
    )

    parser.add_argument('--images_folder', default='./data/media')
    parser.add_argument('--export_folder', default='./object_detection')

    args = parser.parse_args()
    
    # obtain parsed args
    images_folder = args.images_folder
    export_folder = args.export_folder    

    # load a pretrained yoloV5 model from torch hub
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    print("YOLOV5 loading finished!")

    # detect the objects
    detections = detect_objects(folder_path=images_folder, model=model)

