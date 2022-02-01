# TYOLO
Custom trained YOLOv5 for Traffic Light Detection and Distance Estimation

## Train Custom subset of images from COCO dataset
Another approach we tried is to retrain YOLOv5 using only traffic light images from COCO dataset. Since speed is crucial in real-time model, we want the model to be as fast as possible, and one way to achieve that is to cut down on number of classes the model has to classify. The original COCO dataset can classify up to 90 different classes which is an overkill for our use case. To carry out this, we do the following:

1. install fiftyone lib in python.
2. modify Data Processing/load_dataset.py file to load the desired data. The main code that loads the specified classes is below:
   ```
   dataset = foz.load_zoo_dataset(
       "coco-2017",
       split="train",
       label_types=["detections"],
       classes=["traffic light"],
       num_workers=1
   )
   ```
   This will load approximately 4200 images containing traffic lights. However, the images will also have bounding boxes for the other classes.
3. In order to remove the other classes, after saving the loaded dataset, use the View feature to query the data and only annotate traffic light while ignore the remaining classes:
   ```
   view = dataset.filter_labels(
       "ground_truth", F("label").is_in(["traffic light"])
   )
   ```
   Follow the code in Data Processing/test.py file to query and save a new dataset which only contain bounding boxes for Traffic Light
4. Once we have the raw data, now we have to create corresponding text files that complies to COCO standard. FiftyOne library will generate a JSON file with all classes in the images together with their bounding box and coordinates
5. Run Jupyter Notebooks/Data Processing.ipynb and parse in the JSON file, it will create a dataframe for all images with the coresponding coordinates, width and height values for each traffic light in each row in FiftyOne Format
6. Run Jupyter Notebooks/prepare_dataset_format.ipynb and pass in labels.json file generated from fiftyones lib to extract the bounding box for each traffic light for each image. This notebook then normalizes the values into the format used by YOLOv5 and create a the output list of labels. Save this list to a text file
7. Finally, run Data Processing/create_text_files.py and pass in this text file to create all the label file for each image. Make sure to double check the directory folder to follow YOLOv5 directory format.
8. Now that we have prepared the data, follow the Jupyter Notebooks/Custom_train_Yolo.ipynb file to retrain the models. Before that, make sure to create a custom .yaml file under **YoloV5\data\*** directory to specify the parameters of the models 
9. The weight of the model is saved under YoloV5\run\train\exp folder. Use that weight to test on images and check out how well the model has custom trained.

## Steps for Custom Training YOLOv5 with LARA
The steps to train yolov5 on a custom dataset are given here: [ultralytics/yolov5](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data)

The steps can be summarised as follows :
1. Follow the correct directory structure.
    * The yolov5 repository and the dataset folder need to be at the same level.
2. Convert the custom dataset into YOLOv5 compatible format.
    * Change bounding box pixel coordinates from top left and bottom right to image centre and normalize.
    * An individual label txt file for each image having the same name as the image file.
    * Images can be found at [LARA Images](https://drive.google.com/drive/folders/1-0Ve-ibZto2NXYtMEfP35UA65ckS9LZ5?usp=sharing).
    * Custom labels for model v1 [labels v1](https://drive.google.com/drive/folders/1dja8uYBEGppLbm7e3x6zEezyiE-fdqMK?usp=sharing)
    * Custom labels for model v2 [labels_v2](https://drive.google.com/drive/folders/1PtAvjCAfpZQ5sH-LlrY7RM6HnLtE7mei?usp=sharing)
3. Specify the number of classes and class labels in the .yaml file.
4. Run *train.py* inside yolov5 repository.
5. The script retrains yolov5 on the custom dataset and return the weights for the new model.

The script for the same can be found under the [Jupyter Notebooks](https://github.tamu.edu/himanshu-singh/TYOLO/tree/master/Jupyter%20Notebooks) directory.

The weights.pt file obtained in the above step can be used to load our custom model for performing other functions like traffic light detection in videos and distance estimation.

## LARA model v1
In order to train yolo to detect traffic light belonging only to our lane, we used the [LARA Traffic Lights Dataset](http://www.lara.prd.fr/benchmarks/trafficlightsrecognition). The weights obtained for this model can be found inside the [weights](https://github.tamu.edu/himanshu-singh/TYOLO/tree/master/weights) directory. These weights can be used while loading the yolo model in pytorch and can be used for custom applications like traffic like detection in real-time videos and computation of additional features. We first computed the results for this model on real traffic videos to see how the model performed. Our notebooks for traffic light detection on videos can be found at [Video_Detection](https://github.tamu.edu/himanshu-singh/TYOLO/tree/master/Video_Detection)

## LARA model v2
One we were sure that the dataset was a good fit for our model to detect traffic lights, we looked for ways to improve the performance of the model and also tried to come up with features that could help an autonomous vehicle in making real time decisions like when to stop and when to accelerate. The three main improvements that we implemented are
1. We masked the lower 60% of the image while passing it through the model so the number of bounding boxes created was reduced significantly. This improved the performance of the model by 30\% .
2. Then in order to detect the color of traffic light, we modified the labels in our dataset and changed the configurations of our model in the .yaml file to detect two classes instead of one ( go and stop ).
3. We used the distance formula to estimate the distance between the traffic lights and the vehicle without the use of any other sensor value.
    * To calculate the distance we correlated the bounding box height with the height of the actual traffic light and then made use of focal length of the camera to compute actual distance of the object.
![distance formula](https://github.tamu.edu/himanshu-singh/TYOLO/blob/master/distance.png) 
    * The specification of the camera as given in LARA website are **Marling F-046C (@ 25Hz), lens 12mm**.
    * 12 mm was used as the focal length of the camera.
    * to estimate the the source height we used the dots per inch(dpi) as 96. ( (20 pixels x 25.4)/ 96 ) 

These features when combined together would help the vehicle in making real time decisions related to the motion of the vehicle.

The final jupyter notebook with our custom code for identifying traffic lights in videos along with color detection and distance estimation can be found at [video_detection](https://github.tamu.edu/himanshu-singh/TYOLO/blob/master/Video_Detection/Robotics_videomods_2.ipynb)
