from torch.utils.data import Dataset
import os
import cv2
#from vgg_torch_transform import ImageTransform
import numpy as np
import torch

class CustomDataSet(Dataset) :
    def __init__(self, file_path, image_size, transform=None, phase='tran') :
        self.image_path_list = self.extract_file(file_path)
        self.image_label_dict = self.extract_label(file_path)
        self.image_size = image_size
        self.transform = transform
        self.phase = phase

    def __len__(self) :
        return(len(self.image_path_list))


    def __getitem__(self, idx) :
        image_path = self.image_path_list[idx]
        src = cv2.imread(image_path, 1)
        src = cv2.cvtColor(src,cv2.COLOR_BGR2RGB)
        src = cv2.resize(src, (self.image_size, self.image_size), interpolation=cv2.INTER_AREA)
        #dst = self.ImageTransform(src, resize=224)
        src = src /255.
        dst = src.transpose(2, 0, 1) # C, H, W
        #dst = torch.from_numpy(src.astype(np.float32))
        dst = dst.astype(np.float32)
        self.image_path = image_path.replace('\\','/')
        raw_label = self.image_path.split('/')[-2]
        label = self.image_label_dict[raw_label] # number return

        return dst, label

    def extract_file(self, file_path) :
        image_path_list = []
        possible_image_extention = ['.jpg', '.jpeg', ',JPG', '.bmp', '.png']
        for root, dirs, files in os.walk(file_path) :
            if len(files) > 0 :
                for file in files :
                    if os.path.splitext(file)[1] in possible_image_extention :
                        image_path = os.path.join(root, file)
                        image_path = image_path.replace('\\','/')
                        image_path_list.append(image_path)

        return image_path_list

    def extract_label(self, file_path) :
        image_label_dict = {}
        for i, label in enumerate(os.listdir(file_path)) :
            if os.path.isdir(os.path.join(file_path, label)) :
                folder_number = label.split('_')[0]
                image_label_dict[label] = int(folder_number) # plant_name : 0

        return image_label_dict