import os

root = r"./dataset/train"

# 构建所有文件名的列表，dir为label
filename = []
# label = []
dirs = os.listdir(root)
for dir in dirs:
    dir_path = root + '/' + dir
    names = os.listdir(dir_path)
    for n in names:
        filename.append(dir_path + '/' + n + '\t' + dir)

# 分别写入train.txt, test.txt
with open('./dataset/train.txt', 'w') as f1:
    for i in filename:
        f1.write(i + '\n')

print('成功！')
