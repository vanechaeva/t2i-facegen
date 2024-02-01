import pandas as pd
import numpy as np
import torch
import os
import random
from PIL import Image
from tqdm.notebook import tqdm

np.random.seed(0)
torch.manual_seed(0)
class ImageTextDataset(torch.utils.data.Dataset):
    def __init__(self, root_dir, csv, transform=None):
        self.text_df = pd.read_csv(csv, encoding='cp1251')
        self.length = len(self.text_df)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.text_df)

    def __getitem__(self, index):
        if torch.is_tensor(index):
            index = index.tolist()

        img_name = os.path.join(self.root_dir, self.text_df.iloc[index, 0])
        image = Image.open(img_name)
        true_text = self.text_df.iloc[index, 1:].values[0]

        if self.transform:
            true_image = self.transform(image)

        wrong_index = random.randint(0, self.length - 1)
        while wrong_index == index:
            wrong_index = random.randint(0, self.length - 1)
        wrong_img_name = os.path.join(self.root_dir, self.text_df.iloc[wrong_index, 0])
        wrong_image = Image.open(wrong_img_name)

        if self.transform:
            wrong_image = self.transform(wrong_image)

        return true_image, true_text, wrong_image

def process_data(attribute_csv_path):
    attributes_df = pd.read_csv(attribute_csv_path, encoding='cp1251')

    drop_cols = {"Мешки_под_глазами", "Челка", "Размытый", "Безбородый"}
    attributes_df = attributes_df.drop(columns=drop_cols)
    only_attributes = attributes_df.drop(columns="image_id")
    classes = set(only_attributes)
    print("Представленные классы: ", classes)
    print("Количество классов: ", len(classes))

    return only_attributes, classes
