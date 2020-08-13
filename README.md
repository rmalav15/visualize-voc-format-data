# Visualize Voc Dataset
A simple utility python application to visualize pascal voc (format) dataset images with bounding boxes. Useful to check whether there is any error in forming annotation files. 

<img src='./output/hyang_video0_10045.jpg' width="500">

## Requirements
- beautifulsoup4==4.9.1
- install==1.3.3
- lxml==4.5.2
- numpy==1.19.1
- opencv-python==4.4.0.40
- soupsieve==2.0.1

## How to run

```bash
python main.py --root_dir [PASCAL VOC (format) dataset root directory] --type train
```

#### Keyboard Input Usage
- a: previous image
- d: next image
- s: random image
- q: quit program
