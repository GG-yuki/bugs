# data_image = {x:datasets.ImageFolder(root = r"C:\Users\Yuki\Desktop\bugs\python\graduation_design\dog&cat",
#                                      transform = transform)
#               for x in ["train", "val"]}
#
# data_loader_image = {x:torch.utils.data.DataLoader(dataset=data_image[x],
#                                                 batch_size = 4,
#                                                 shuffle = True)
#                      for x in ["train", "val"]}
# classes = data_image["train"].classes
# classes_index = data_image["train"].class_to_idx
# print(classes)
# print(classes_index)
# print(len(data_image["train"]))
# print(len(data_image["val"]))

