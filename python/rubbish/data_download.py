import torchvision.datasets as datasets
import torchvision.transforms as transforms

data_transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])


trainsata = datasets.ImageFolder(root="/home/jiqiwei/My_project/imagenet_data/data",transform=data_transform,train =True,download=True)

