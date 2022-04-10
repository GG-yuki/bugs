from mobilenetv3_another_sobel import *
import torch


def main():
    model = mobilenet_v3_small(pretrained=False, num_classes=100)
    x = torch.randn(2, 3, 224, 224)
    y = model(x)
    print(y.size())


if __name__ == '__main__':
    main()
