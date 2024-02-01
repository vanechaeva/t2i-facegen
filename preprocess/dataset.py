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

def generate_weights(arr, num_classes):
    counts = np.zeros(num_classes)
    for row in tqdm(arr):
        indexes = np.where(row == 1)
        counts[indexes] += 1
    N = float(sum(counts))
    weight_per_class = np.zeros(num_classes)
    for i in range(num_classes):
        weight_per_class[i] = N / counts[i]
    weights = [0.0] * len(arr)
    for i, row in tqdm(enumerate(arr)):
        indexes = np.where(row == 1)
        weights[i] = sum(weight_per_class[indexes])
    return weights

def get_weighted_dataloader(
    attribute_csv_path,
    image_location = None,
    text_desc_location = None,
    transform = None,
    subset_size = 10000,
    batch_size = 64,
):
    random_indices = torch.randperm(subset_size)
    only_attributes, classes = process_data(attribute_csv_path)
    only_attributes = only_attributes.iloc[random_indices]
    print("Длина подмножества данных:", len(only_attributes))

    weights = generate_weights(only_attributes.values, len(classes))
    sampler = torch.utils.data.sampler.WeightedRandomSampler(weights, len(weights))

    dataset = ImageTextDataset(
        image_location, text_desc_location, transform=transform
    )

    subset_dataset = torch.utils.data.Subset(dataset, random_indices)

    weighted_dataloader = torch.utils.data.DataLoader(
        subset_dataset,
        batch_size = batch_size,
        shuffle = False,
        sampler = sampler,
        pin_memory = True,
    )

    return weighted_dataloader, iter(weighted_dataloader)
