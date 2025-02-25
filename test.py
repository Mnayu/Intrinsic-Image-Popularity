# -*- coding: utf-8 -*-
import argparse
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import glob
import numpy as np
import pandas as pd

def prepare_image(image):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    Transform = transforms.Compose([
            transforms.Resize([224,224]),      
            transforms.ToTensor(),
            ])
    image = Transform(image)   
    image = image.unsqueeze(0)
    return image.to(device)

def predict(image, model):
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    print(r'Filename: {}- Popularity Rating: {}'.format(filename,preds.item()))

root_dir = "root_directory"


if __name__ == '__main__':
    for filename in glob.iglob(root_dir + '**/*.jpg', recursive=True):
        parser = argparse.ArgumentParser()
        parser.add_argument('--image_path', type=str, default=filename)
        config = parser.parse_args()
        image = Image.open(config.image_path)
        model = torchvision.models.resnet50()
        # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input
        model.fc = torch.nn.Linear(in_features=2048, out_features=1)
        model.load_state_dict(torch.load('C:/Users/abhim/Desktop/personal-projects/Intrinsic-Image-Popularity-master/Intrinsic-Image-Popularity-master/model/model-resnet50.pth', map_location=device)) 
        model.eval().to(device)
        predict(image, model)
