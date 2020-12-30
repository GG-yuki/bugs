import torch
print('available gpus is ', torch.cuda.device_count(), torch.cuda.get_device_name())