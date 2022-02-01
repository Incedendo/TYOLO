import os
from shutil import copyfile


img_set = set()

with open('text.txt') as f:
    lines = f.readlines()

    for line in lines:
        img_filename = line[:17]
        img_set.add(img_filename[:16])

        text_file = img_filename[:12] + '.txt'
        content = line[17:]

        # print(text_file)
        # print(content)

        # print(content)
        dir_labels = 'K:\TAMU\Fall 2021\Robotics & Spatial Intelligence\YOLO\CocoTrafficDataSet\dataset\labels\\'
        dir_images = 'K:\TAMU\Fall 2021\Robotics & Spatial Intelligence\YOLO\CocoTrafficDataSet\dataset\images\\'

        # file = 'K:\TAMU\Fall 2021\Robotics & Spatial Intelligence\YOLO\CocoTrafficDataSet\dataset\labels\\' + text_file
        
        isExist = os.path.exists(dir_images)
        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(dir_images)

        # # file_exists = os.path.exists(path_to_file)

        # with open(file, 'a') as f2:
        #     f2.write(content)

print(img_set)

image_dir = 'K:\TAMU\Fall 2021\Robotics & Spatial Intelligence\CocoData\\val2017'
for root, dirs, files in os.walk(image_dir):
    for name in files:
        if name in img_set:
            print(os.path.join(root, name))
            src = os.path.join(root, name)
            dst = 'K:\TAMU\Fall 2021\Robotics & Spatial Intelligence\YOLO\CocoTrafficDataSet\dataset\images\\' + name
            print(dst + '\n')
            copyfile(src, dst)
#    for name in dirs:
#       print(os.path.join(root, name))