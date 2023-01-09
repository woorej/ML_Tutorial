import torch
import cv2
import numpy as np
import torch.nn.functional as F
import os
from resnet_model import *

import time

with open("label.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def model_test(model, file_path, image_size) :
    image_path_list = []
    possible_image_extention = ['.jpg', '.jpeg', ',JPG', '.bmp', '.png']
    for root, dirs, files in os.walk(file_path) :
        if len(files) > 0 :
            for file in files :
                if os.path.splitext(file)[1] in possible_image_extention :
                    image_path = os.path.join(root, file)
                    image_path = image_path.replace('\\','/')
                    image_path_list.append(image_path)
    
    print(image_path_list)

    for img_path in image_path_list :
        img = cv2.imread(img_path, 1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (image_size, image_size), interpolation=cv2.INTER_AREA)
        img = img /255.
        
        img = img.transpose(2, 0, 1).astype(np.float32)
        # img = np.ascontiguousarray(img)
        img = np.expand_dims(img, axis=0)
        img = torch.Tensor(img)
        model.eval()
        outputs = model(img)

        #print(outputs)
        preds = F.softmax(outputs[0], dim=0)
        index = torch.argmax(preds)
        print(categories[index])


test_path = './plant_dataset/Test'
size = 224
model = resnet50()
model.load_state_dict(torch.load('./weights/plant/2023-01-09/weights_before_0.9574_after_0.9596_07.pth'))
#model = torch.load('./weights_0.6015_0.6059_18.pth')
#print(summary_(model,(3,224,224),batch_size=1))
model_test(model, test_path, image_size=size)
