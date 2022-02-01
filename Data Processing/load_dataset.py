import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewField as F

# print(fo.config.dataset_zoo_dir)
fo.config.dataset_zoo_dir = "K:\\TAMU\\coco"
print(fo.config.dataset_zoo_dir)
print(fo.list_datasets())

# delete a dataset 

#######################################################################################
## Delete an existing dataset in repo
# test = fo.load_dataset("coco-2017-train-1")
# test.delete()

#######################################################################################
## Load a dataset from coco-2017 source

# dataset = foz.load_zoo_dataset(
#     "coco-2017",
#     split="train",
#     label_types=["detections"],
#     classes=["traffic light"],
#     
#     num_workers=1
# )

#######################################################################################
## Load dataset from existing datasets

# dataset = fo.load_dataset("train_traffic_light_dataset")

dataset = fo.load_dataset("coco-2017-train")
# Now the dataset is permanent
# dataset.persistent = True

# schema = dataset.get_field_schema()
# print(schema)

# print(dataset.classes)

#######################################################################################
## create custom view from dataset

# view = dataset.filter_labels(
#     "ground_truth", F("label").is_in(["traffic light"])
# )
# view.save()

#######################################################################################
## Create a new dataset from view

# train_traffic_light_dataset = view.clone('train_traffic_light_dataset')
# train_traffic_light_dataset.persistent = True

session = fo.launch_app(dataset)
# session.view = view
session.wait()