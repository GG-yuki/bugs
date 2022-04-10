import zipfile
import numpy as np
from PIL import Image
from torchvision.datasets import ImageFolder


class YFCC100M_dataset(ImageFolder):
    """
    YFCC100M dataset.
    """

    def __init__(self, root, size, transform=None):
        super(YFCC100M_dataset, self).__init__(root, size, transform)
        self.root = root
        self.transform = transform
        self.sub_classes = None

        # remove data with uniform color and data we didn't manage to download
        self.indexes = np.arange(size)

        # for subsets
        self.subset_indexes = None

    def __getitem__(self, ind):
        index = ind
        if self.subset_indexes is not None:
            index = self.subset_indexes[ind]
        index = self.indexes[index]

        path, target = self.samples[index]
        sample = self.loader(path)

        # apply transformation
        if self.transform is not None:
            sample = self.transform(sample)

        # id of cluster
        sub_class = -100
        if self.sub_classes is not None:
            sub_class = self.sub_classes[ind]

        return sample, sub_class

    def __len__(self):
        if self.subset_indexes is not None:
            return len(self.subset_indexes)
        return len(self.indexes)
