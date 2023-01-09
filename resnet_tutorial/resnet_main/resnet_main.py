from resnet_model import *
from resnet_dataloader import CustomDataSet
from tqdm import tqdm
import torch
import time
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader
import os
from datetime import date
from torch.utils.tensorboard import SummaryWriter
#from resnet_logger import *
#from resnet_logger import get_logger
import yaml
import logging.handlers
from tqdm import tqdm

log_config_path = './parameter_info.yaml'

if os.path.exists(log_config_path) :
    with open(log_config_path, 'r') as f :
        cfg = yaml.full_load(f.read())


class TqdmLoggingHandler(logging.Handler):
    def init(self, level=logging.NOTSET):
        super().init(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)

def get_logger():
    logger = logging.getLogger('vga_train') # logger 생성 
    if len(logger.handlers) > 0: return logger 
    logger.setLevel(logging.DEBUG) # 출력 기준 설정 

    file_handler = logging.handlers.TimedRotatingFileHandler(
    filename='log/train.log', when='midnight', interval=1,  encoding='utf-8'
    )
    file_handler.prefix = 'log-%Y%m%d' # 파일명 끝에 붙여줌; ex. log-20190811
    formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(TqdmLoggingHandler())
    # logger.propagate = False
    logger.info(cfg)
    return logger


def train_model(model, dataloader_dict, criterion, optimizer, scheduler, lr, num_epoch, patience_limit) :

    best_acc = 0.0
    best_val_loss = 100.0
    patience_check = 0

    writer = SummaryWriter()
    since = time.time()
    logger = get_logger()

    for epoch in range(num_epoch) :
        #print(f'Epoch {epoch+1}/{num_epoch}')
        logger.info("="*90)
        logger.info(f"Epoch {epoch+1}/{num_epoch}")
        print('-'*20)

        for phase in ['train', 'validation'] :
            if phase == 'train' :
                model.train()
                logger.info(f"{phase}")
            else :
                model.eval()
                logger.info(f"{phase}")

            epoch_loss = 0.0
            epoch_corrects = 0

            for inputs, labels in tqdm(dataloader_dict[phase]) :
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad() 
                with torch.set_grad_enabled(phase=='train') :
                    outputs = model(inputs) 
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train' :
                        loss.requires_grad_(True)
                        loss.backward() 
                        optimizer.step()

                    # input.size(0) -> batch_size
                    epoch_loss = epoch_loss + loss.item()*inputs.size(0) # 異쒕젰寃곌낵��� �젅�씠釉붿쓽 �삤李⑤�� 怨꾩궛�븳 寃곌낵瑜� �늻�쟻
                    epoch_corrects = epoch_corrects + torch.sum(preds==labels.data)
            
            epoch_acc = epoch_corrects.double() / len(dataloader_dict[phase].dataset)
            epoch_loss = epoch_loss / len(dataloader_dict[phase].dataset)

            if phase == 'train' :
                writer.add_scalar("Loss/train", epoch_loss, epoch)
                writer.add_scalar("Acc/train", epoch_acc, epoch)
            else :
                writer.add_scalar("Loss/validation", epoch_loss, epoch)
                writer.add_scalar("Acc/validation", epoch_acc, epoch)

            logger.info(f"{phase} Loss:{epoch_loss:.4f} Acc:{epoch_acc:.4f}")
            # print(f"{phase} Loss:{epoch_loss:.4f} Acc:{epoch_acc:.4f}")
            
            # best_acc = 0, save best weights(watch -> val acc)
            if phase == 'validation' and epoch_acc > best_acc :
                temp = best_acc
                best_acc = epoch_acc
                best_model_wts = model.state_dict()

                print("="*40,"Model Check Point Working","="*40)
                print(f"before_acc:{temp:.4f} -> after_acc:{epoch_acc:.4f}")

                today = date.today()
                today_str = today.strftime('%Y-%m-%d')
                data_set_name = "plant"
                today_weight_path = f"./weights/{data_set_name}/{today_str}" # ./weights/plant/2023-01-04/
                os.makedirs(today_weight_path, exist_ok=True)

                save_path = today_weight_path+f"/weights_before_{temp:.4f}_after_{best_acc:.4f}_{epoch:02d}.pth"
                torch.save(best_model_wts, save_path)

             # early stopping
            if phase == 'validation' and epoch_loss > best_val_loss:
                print('#'*20,'Early Stopping Working',"#"*20)
                patience_check += 1

                if patience_check >= patience_limit: # early stopping
                    return
            else: 
                best_loss = epoch_loss
                patience_check = 0

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

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
model = resnet50().to(device)

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
size = cfg['image_size']
batch_size = cfg['batch_size']
num_epoch = cfg['num_epoch']
patience_limit = cfg['patience_limit']

# Dataset
train_dataset = CustomDataSet(train_image_path,image_size=size, transform=None, phase='train')
val_dataset = CustomDataSet(val_image_path, image_size=size, transform=None, phase='validation')

# Data Loader
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

dataloader_dict = {'train':train_dataloader,'validation':val_dataloader}

#print(train_dataset.extract_label(train_image_path))
output_model = train_model(model, dataloader_dict, criterion, optimizer, scheduler, lr, num_epoch, patience_limit)
