# Collaborate Respoitory
This repository is for many kinds of project collaborating project

# data_loader
Data Handler from AI task organized by Korea Customs Service

# vgg_tutorial
- Dataset : plant_dataset
- model : vgg16
- function
  - learning rate scheduler - ReduceLROnPlateau
  - save best acc weight
  - you can see train/val processing on tensorboard
      use this command: tensorboard --logdir=runs

# resnet_tutorial
- Dataset : plant_dataset
- model : resnet50
- function
  - same as vgg_tutorial function
  - used logger handler
  - used config.yaml to give a paramter value
  - early stopping
