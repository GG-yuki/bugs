import sys
import os.path
 
if __name__ == "__main__":
 
    f = open('label.txt', 'w')
    # 文件名，文件下还有多个类别的文件。
    #BASE_PATH="JAFFE"
    SEPARATOR=" " 
    # 绝对路径地址
    pth = r'/home/jijl/My_project/jianc/warship/train'
 
    for dirname, dirnames, filenames in os.walk(pth):
        for subdirname in dirnames:
            if subdirname == 'beach':
                label = 0
            else:
                label = 1
            #label = subdirname
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                #abs_path = pth + abs_path
                #print "%s%s%s" % (abs_path, SEPARATOR, label)
                f.write("%s%s%s\n"%(abs_path, SEPARATOR, label))
    f.close()