import pickle

import numpy as np
import rasterio
import torch
import torch.nn as nn
from osgeo import gdal

# Initialize the model, loss function, and optimizer
device = torch.device("cpu")


class FeedForwardNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(FeedForwardNN, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# Function to extract features from the bands
def extract_features_from_bands(red_band, nir_band, swir_band):
    # Calculate the mean value for each band
    red_mean = np.mean(red_band)
    nir_mean = np.mean(nir_band)
    swir_mean = np.mean(swir_band)

    return [red_mean, nir_mean, swir_mean]


# Function to predict the class using the features
def predict_from_features(features, model, scaler):
    # Normalize the features
    features = scaler.transform([features])

    # Convert the features to a PyTorch tensor
    features_tensor = torch.tensor(features, dtype=torch.float32).to(device)
    # Load the saved scaler
    scaler_path = "./scalerbest.pkl"
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    model_path = "./FeedForwardBest.pt"
    model = FeedForwardNN(input_dim=3, hidden_dim=64, output_dim=9)
    model.load_state_dict(torch.load(model_path))
    # Pass the tensor through the model
    model.to(device)
    model.eval()
    with torch.no_grad():
        output = model(features_tensor)

    # Interpret the output
    _, predicted_class = torch.max(output.data, 1)
    return predicted_class.item()


def predict_from_raster_bands(red_path, nir_path, swir_path):
    # Read the raster bands as NumPy arrays
    with rasterio.open(red_path) as r:
        red_band = r.read()
    with rasterio.open(nir_path) as n:
        nir_band = n.read()
    with rasterio.open(red_path) as s:
        swir_band = s.read()

    # Extract the features from the bands
    features = extract_features_from_bands(red_band, nir_band, swir_band)

    # Load the saved scaler
    scaler_path = "./scalerbest.pkl"
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    # Initialize the model
    model_path = "./FeedForwardBest.pt"
    model = FeedForwardNN(input_dim=3, hidden_dim=64, output_dim=9)
    model.load_state_dict(torch.load(model_path))

    # Predict the class using the features
    predicted_class = predict_from_features(features, model, scaler)

    return predicted_class
