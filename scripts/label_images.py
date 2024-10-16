import torch, cv2, psycopg2
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
            
            # Get the class name from the model
            class_name = model.names[int(cls)]

            detections.append({
                'media_path': path,
                'label': class_name,
                'confidence': conf,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2
            })
    
    # convert the list of dicts into a dataframe
    detections = pd.DataFrame(data=detections)

    return detections

def push_detections(detections: pd.DataFrame, table_name: str, host: str, username: str, password: str, database: str, port: int):
    """
    Push the detections dataframe to a PostgreSQL table using psycopg2.

    Args:
        detections (pd.DataFrame): DataFrame containing detection results.
        table_name (str): The name of the table to insert data into.
        host (str): The PostgreSQL server host.
        username (str): PostgreSQL username.
        password (str): PostgreSQL password.
        database (str): Name of the PostgreSQL database.
        port (int): Port number for PostgreSQL.
    """
    # Establish connection
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        cursor = connection.cursor()
    except Exception as e:
        print(f"Failed to establish connection: {e}")
        return

    # Generate insert query
    insert_query = f"INSERT INTO {table_name} (media_path, label, confidence, x1, y1, x2, y2) VALUES %s"

    # Prepare data for insertion
    values = []
    for _, row in detections.iterrows():
        values.append((row['media_path'], row['label'], row['confidence'], row['x1'], row['y1'], row['x2'], row['y2']))

    try:
        # Use psycopg2.extras.execute_values for bulk insert
        from psycopg2.extras import execute_values
        execute_values(cursor, insert_query, values)
        
        connection.commit()
        print(f"Successfully pushed {len(detections)} records to {table_name}.")
    except Exception as e:
        print(f"Failed to execute query: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    import argparse, os, warnings
    from dotenv import load_dotenv

    # disable warning
    warnings.simplefilter(action='ignore')

    # define argument for providing the path to images folder and path to export detections into plus the .env file.
    parser = argparse.ArgumentParser(
        prog="Object Detector",
        description="A script that "
    )

    parser.add_argument('--images_folder', default='./data/media')
    parser.add_argument('--export_folder', default='./object_detection')
    parser.add_argument('--env', default='.env')

    args = parser.parse_args()
    
    # obtain parsed args
    images_folder = args.images_folder
    export_folder = args.export_folder
    env_path = args.env    
    
    # load the database connection params from the .env
    load_dotenv(dotenv_path=env_path)
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    # load a pretrained yoloV5 model from torch hub
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    print("YOLOV5 loading finished!")

    # detect the objects
    detections = detect_objects(folder_path=images_folder, model=model)

    # push to the database
    push_detections(detections=detections, table_name="image_detection", host=host, username=username, password=password, database=db_name, port=port)
