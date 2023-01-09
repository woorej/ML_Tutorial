from torchvision import transforms

class ImageTransform() :
    def __init__(self, resize) :
        self.data_transform = {
            'train' : transforms.Compose([
                transforms.RandomResizedCrop(resize),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
            ]),
            'val' : transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(resize),
                transforms.ToTensor(),
            ])

        }
    
    def __call__(self, img, phase) :
        return self.data_transform[phase](img)