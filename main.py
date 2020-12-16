import os
import argparse
import random
from data import Data
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", type=str, default="/mnt/069A453E9A452B8D/Ram/surveillance-data/sdd_train")
parser.add_argument("--type", type=str, default="train", help="train|val|trainval|test")
parser.add_argument("--random_seed", type=int, default=100)
parser.add_argument("--save_images", type=bool, default=True)
parser.add_argument("--save_dir", type=str, default="output")
parser.add_argument("--line_thickness", type=int, default=1)
parser.add_argument("--with_mask",action="store_true")
parser.add_argument("--with_bbox",action="store_true")
args = parser.parse_args()
random.seed(args.random_seed)

img_dir = os.path.join(args.root_dir, 'JPEGImages')
ann_dir = os.path.join(args.root_dir, 'Annotations')
set_dir = os.path.join(args.root_dir, 'ImageSets', 'Main')
mask_dir=os.path.join(args.root_dir,'SegmentationClass')


def get_image_list(dir, filename):
    image_list = open(os.path.join(dir, filename)).readlines()
    return [image_name.strip() for image_name in image_list]


def process_image(image_data,with_mask=False,with_bbox=False):
    if not os.path.exists(image_data.image_path):
        image_data.image_path=image_data.image_path.replace('jpg','png')
    image = cv2.imread(image_data.image_path)
    image = cv2.putText(image, image_data.image_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    if with_bbox:
        for ann in image_data.annotations:
            box_color = (0, 255, 0)  #Green
            if ann.difficult or ann.truncated:
                box_color = (0, 0, 255) #Red
            image = cv2.rectangle(image, (ann.xmin, ann.ymin), (ann.xmax, ann.ymax), box_color, args.line_thickness)
            image = cv2.putText(image, ann.name, (ann.xmin, ann.ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    if with_mask:
        if os.path.exists(image_data.mask_path):
            mask_img=cv2.imread(image_data.mask_path)
            image=cv2.addWeighted(image,1,mask_img,1,0.0)
    return image


def main(args):
    image_list = get_image_list(set_dir, args.type + ".txt")
    total_images = len(image_list)

    index = random.randint(0, total_images)
    while True:
        image_data = Data(args.root_dir, image_list[index])
        image = process_image(image_data,args.with_mask,args.with_bbox)
        if args.save_images:
            cv2.imwrite(os.path.join(args.save_dir, image_list[index] + ".jpg"), image)
        cv2.imshow('image', image)
        k = chr(cv2.waitKey())
        if k == 'd':  # next
            index = index + 1 if index != total_images - 1 else 0
        elif k == 'a':
            index = index - 1 if index != 0 else total_images - 1
        elif k == 's':
            index = random.randint(0, total_images)
        elif k == 'q':
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break


if __name__ == '__main__':
    main(args)
