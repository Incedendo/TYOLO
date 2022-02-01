import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewField as F

# print(fo.config.dataset_zoo_dir)
fo.config.dataset_zoo_dir = "K:\\TAMU\\coco"
print(fo.config.dataset_zoo_dir)
print(fo.list_datasets())

dataset = fo.load_dataset("train_traffic_light_dataset")

# The directory to which to write the exported dataset
export_dir = "K:\TAMU\Fall 2021\Robotics & Spatial Intelligence\YOLO\TraficLightDataset"

# The name of the sample field containing the label that you wish to export
# Used when exporting labeled datasets (e.g., classification or detection)
label_field = "ground_truth"  # for example

# The type of dataset to export
# Any subclass of `fiftyone.types.Dataset` is supported
dataset_type = fo.types.COCODetectionDataset  # for example

# Export the dataset!
dataset.export(
    export_dir=export_dir,
    dataset_type=dataset_type,
    label_field=label_field,
)