
from vgg_model import *
from vgg_torch_loader import CustomDataSet
from tqdm import tqdm
import torch
import time
import torch.nn as nn
from vgg_torch_transform import ImageTransform
from torch import optim
from torch.utils.data import DataLoader
import os
import cv2
import numpy as np
from datetime import date
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter

def train_model(model, dataloader_dict, criterion, optimizer, scheduler, lr, num_epoch) :

    since = time.time()
    best_acc = 0.0
    best_train_acc = 0.0

    writer = SummaryWriter()

    for epoch in range(num_epoch) :
        print(f'Epoch {epoch+1}/{num_epoch}')
        print('-'*20)

        for phase in ['train', 'validation'] :
            if phase == 'train' :
                model.train()
            else :
                model.eval()

            epoch_loss = 0.0
            epoch_corrects = 0

            for inputs, labels in tqdm(dataloader_dict[phase]) :
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad() # 기울기를 0으로 설정
 
                with torch.set_grad_enabled(phase=='train') :
                    outputs = model(inputs) # 순전파 학습
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train' :
                        loss.requires_grad_(True)
                        loss.backward() # 역전파 학습
                        optimizer.step()

                    # input.size(0) -> batch_size
                    epoch_loss = epoch_loss + loss.item()*inputs.size(0) # 출력결과와 레이블의 오차를 계산한 결과를 누적
                    epoch_corrects = epoch_corrects + torch.sum(preds==labels.data)
            
            epoch_acc = epoch_corrects.double() / len(dataloader_dict[phase].dataset)
            epoch_loss = epoch_loss / len(dataloader_dict[phase].dataset)

            if phase == 'train' :
                writer.add_scalar("Loss/train", epoch_loss, epoch)
                writer.add_scalar("Acc/train", epoch_acc, epoch)
            else :
                writer.add_scalar("Loss/validation", epoch_loss, epoch)
                writer.add_scalar("Acc/validation", epoch_acc, epoch)

            print(f"{phase} Loss:{epoch_loss:.4f} Acc:{epoch_acc:.4f}")
            
            # 처음 best_acc = 0, save best weights(watch -> val acc)
            if phase == 'validation' and epoch_acc > best_acc :
                temp = best_acc
                best_acc = epoch_acc
                best_model_wts = model.state_dict()

                print("="*40,"Model Check Point Working","="*40)
                print(f"epoch_acc:{epoch_acc:.4f}, best_val_acc:{best_acc:.4f}")

                today = date.today()
                today_str = today.strftime('%Y-%m-%d')
                data_set_name = "plant"
                today_weight_path = f"./weights/{data_set_name}/{today_str}" # ./weights/plant/2023-01-04/
                os.makedirs(today_weight_path, exist_ok=True)

                save_path = today_weight_path+f"/weights_before_{temp:.4f}_after_{best_acc:.4f}_{epoch:02d}.pth"
                torch.save(best_model_wts, save_path)

            # learning rate scheduler
            if phase == 'validation' :
                scheduler.step(epoch_loss)
                print('='*40,'lr scheduler working','='*40)
                print('before lr', lr)
                print('current lr:',optimizer.param_groups[0]['lr'])

    time_elapsed = time.time() - since

    print(f'Training Complete in {time_elapsed//60:.0f}m {time_elapsed%60:.0f}s')
    print(f"Best val Acc:{best_acc}")

    writer.flush()
    return model

cfgs = {
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'], #13 + 3 = vgg 16
}

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
model = vgg16().to(device)

criterion = nn.CrossEntropyLoss().to(device)
lr = 0.0001
optimizer = optim.Adam(model.parameters(), lr=lr)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer=optimizer,
    factor=0.5,
    patience=10,
    verbose=1,
    threshold=1e-4,
    mode='min',
    cooldown=5,
    min_lr=1e-8
)

# define value
train_image_path = './plant_dataset/train/'
val_image_path = './plant_dataset/validation/'
test_path = './plant_dataset/Test'
size = 224
batch_size = 64
num_epoch = 30


# Dataset
train_dataset = CustomDataSet(train_image_path,image_size=size, transform=None, phase='train')
val_dataset = CustomDataSet(val_image_path, image_size=size, transform=None, phase='validation')

# Data Loader
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

dataloader_dict = {'train':train_dataloader,'validation':val_dataloader}

print(train_dataset.extract_label(train_image_path))
output_model = train_model(model, dataloader_dict, criterion, optimizer, scheduler, lr, num_epoch)
