import os
import argparse
import random
from data import Data
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", type=str, default="/mnt/069A453E9A452B8D/Ram/surveillance-data/sdd_train")
parser.add_argument("--type", type=str, default="train", help="train|val|trainval|test")
parser.add_argument("--random_seed", type=int, default=1000)
parser.add_argument("--label_set", type=str, default="")
parser.add_argument("--line_thickness", type=int, default=5)
args = parser.parse_args()
random.seed(args.random_seed)

img_dir = os.path.join(args.root_dir, 'JPEGImages')
ann_dir = os.path.join(args.root_dir, 'Annotations')
set_dir = os.path.join(args.root_dir, 'ImageSets', 'Main')


def get_image_list(dir, filename):
    image_list = open(os.path.join(dir, filename)).readlines()
    return [image_name.strip() for image_name in image_list]


def process_image(image_data):
    image = cv2.imread(image_data.image_path)
    for ann in image_data.annotations:
        image = cv2.rectangle(image, (ann.xmin, ann.ymin), (ann.xmax, ann.ymax), (0, 255, 0), args.line_thickness)
        image = cv2.putText(image, ann.name, (ann.xmin, ann.ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return image


def main(args):
    image_list = get_image_list(set_dir, args.type + ".txt")
    total_images = len(image_list)

    index = random.randint(0, total_images)
    while True:
        image_data = Data(args.root_dir, image_list[index])
        image = process_image(image_data)
        cv2.imshow('image', image)
        k = chr(cv2.waitKey())
        if k == 'd':  # next
            index = index + 1 if index != total_images - 1 else 0
        elif k == 'a':
            index = index - 1 if index != 0 else total_images - 1
        elif k == 's':
            index = random.randint(0, total_images)
        elif k == 27:
            cv2.waitKey(2)
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main(args)
