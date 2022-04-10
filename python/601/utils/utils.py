import torch as th
import numpy as np


def setup_seed():
    seed = 256849
    print("seed:" + str(seed))
    th.manual_seed(seed)
    th.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    th.backends.cudnn.deterministic = True


def select_action(input_tensor, mask=1, sample=True):
    input_tensor = th.exp(input_tensor.squeeze()) * mask
    prob = input_tensor / th.sum(input_tensor)

    if sample:
        try:
            a = prob.multinomial(1).item()
        except RuntimeError as e:
            print(e)
            # print('prob:', prob)
            # print('input:', input_tensor)
            # print('mask:', mask)
            a = prob.argmax(-1).item()

    else:
        a = prob.argmax(-1).item()
    # return a, th.log(prob)[a].item()
    return a, prob[a].item()

# def select_action(output, mask=1):
#     # output = output.squeeze()
#     tmp = th.exp(output) * mask / th.sum(th.exp(output) * mask, dim=(1,), keepdim=True)
#     return tmp, output[tmp].item()
