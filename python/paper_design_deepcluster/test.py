import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of DeepCluster')
    parser.add_argument('--exp', type=str, default=r'/home/jijl/My_project/paper_design_deepcluster/check', help='path to exp folder')
    return parser.parse_args()

def main(args):
    exp_check = os.path.join(args.exp, 'checkpoints')
    if not os.path.isdir(exp_check):
        os.makedirs(exp_check)
        print('ok')

if __name__ == '__main__':
    args = parse_args()
    main(args)