from ultralytics import YOLO

import cv2


model_path = 'C:/Users/tvrr28/semantc_segmentation/train6/weights/last.pt'

image_path = 'C:/Users/tvrr28/semantc_segmentation/data/images/val/tigers (41).jpg'

img = cv2.imread(image_path)
H, W, _ = img.shape

model = YOLO(model_path)

results = model(img)

for result in results:
    for j, mask in enumerate(result.masks.data):

        mask = mask.numpy() * 255

        mask = cv2.resize(mask, (W, H))

        cv2.imwrite('./output.png', mask)