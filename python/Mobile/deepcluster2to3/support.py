"""
/********************************************************************
*
*  文件名：support.py
*
*  文件描述：封装类
*
*  创建人： qiwei_ji, 2020年10月4日
*
*  版本号：1.2
*
*  修改记录：64
*
********************************************************************/
"""
import time
from torchvision import transforms
from util import *
import torch
import numpy as np


# 保存网络
def save_net(net, epoch):
    torch.save(net, './pkl/epoch_%d_net.pkl' % epoch)  # 保存整个网络
    torch.save(net.state_dict(), './pkl/epoch_%d_net_params.pth' % epoch)  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def load_net(net):
    # restore entire net1 to net2
    model_load = torch.load('./pkl/epoch_' + net + '_net.pkl')
    return model_load


# 图像归一化后裁剪，最后尺寸224*224*3
def transform():
    data_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    return data_transform


def write_result(model, epochs, batch_size, num_workers, lr, max_acc, weight_decay, traintime, testtime):
    f = open('./experiment_record(first)/' + model + '/final_result.txt', "a")
    f.write('model %s   train %d epoch   batch_size %d   num_workers %d   lr %f   max_acc: %.3f  '
            'weight_decay %f   traintime %d   testtime %d\n' %
            (model, epochs, batch_size, num_workers, lr, max_acc, weight_decay, traintime, testtime))
    f.close()


def compute_features(dataloader, model, N, batch):
    features = 0
    batch_time = AverageMeter()
    end = time.time()
    model.eval()
    # discard the label information in the dataloader
    for i, (input_tensor, _) in enumerate(dataloader):
        input_var = torch.autograd.Variable(input_tensor.cuda())
        aux = model(input_var).data.cpu().numpy()

        if i == 0:
            features = np.zeros((N, aux.shape[1]), dtype='float32')

        aux = aux.astype('float32')
        if i < len(dataloader) - 1:
            features[i * batch: (i + 1) * batch] = aux
        else:
            # special treatment for final batch
            features[i * batch:] = aux

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % 200 == 0:
            print('{0} / {1}\t'
                  'Time: {batch_time.val:.3f} ({batch_time.avg:.3f})'
                  .format(i, len(dataloader), batch_time=batch_time))
    return features


# 定义训练过程
def train(loader, model, crit, opt, epoch, lr, wd):
    batch_time = AverageMeter()
    losses = AverageMeter()
    data_time = AverageMeter()

    # switch to train mode
    model.train()

    # create an optimizer for the last fc layer
    optimizer_tl = torch.optim.SGD(
        model.top_layer.parameters(),
        lr=lr,
        weight_decay=10 ** wd,
    )

    end = time.time()
    for i, (input_tensor, target) in enumerate(loader):
        data_time.update(time.time() - end)

        target = target.cuda()
        input_var = torch.autograd.Variable(input_tensor.cuda())
        target_var = torch.autograd.Variable(target)

        output = model(input_var)
        loss = crit(output, target_var)

        # record loss
        losses.update(loss.item(), input_tensor.size(0))

        # compute gradient and do SGD step
        opt.zero_grad()
        optimizer_tl.zero_grad()
        loss.backward()
        opt.step()
        optimizer_tl.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        print('Loss: {loss.val:.4f} ({loss.avg:.4f})'.format(loss=losses))
        # 'Epoch: [{0}][{1}/{2}]\t'
        #         #       'Time: {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
        #         #       'Data: {data_time.val:.3f} ({data_time.avg:.3f})\t'
        #         #       'Loss: {loss.val:.4f} ({loss.avg:.4f})'
        #         #       .format(epoch, i, len(loader), batch_time=batch_time,
        #         #               data_time=data_time, loss=losses))

        if (epoch + 1) % 20 == 0:
            print('Loss: {loss.val:.4f} ({loss.avg:.4f})'.format(loss=losses))

        if (epoch + 1) % 50 == 0:
            # lr = lr / 8
            print('save model')
            save_net(model, epoch)

    return losses.avg


def seed(seeds):
    torch.manual_seed(seeds)
    torch.cuda.manual_seed_all(seeds)
    np.random.seed(seeds)


def sava_params(epoch, model, optimizer, net):
    torch.save({'epoch': epoch + 1,
                'state_dict': model.state_dict(),
                'optimizer': optimizer.state_dict()},
               r'./exp/checkpoint_'+net+'.pth.tar')
