import torch
a = torch.randn(2,3).to('cuda')
a = a.cpu()
print(a.numpy()[0])