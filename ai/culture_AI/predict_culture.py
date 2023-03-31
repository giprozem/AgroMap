import numpy as np
import rasterio
import torch
import torch.nn as nn
from scipy import stats
from sklearn.preprocessing import MinMaxScaler


class EncoderDecoderLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(EncoderDecoderLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.encoder_lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.decoder_lstm = nn.LSTM(hidden_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)

        _, (hn, cn) = self.encoder_lstm(x.unsqueeze(1), (h0, c0))  # Add a dimension for the sequence length
        out, _ = self.decoder_lstm(hn.transpose(0, 1), (hn, cn))  # Transpose hn to match the expected input shape
        out = self.fc(out.squeeze(1))  # Squeeze the sequence length dimension
        out = self.relu(out)  # Apply ReLU activation function to the output of the linear layer

        return out


def test_model(red, nir, swir, device=torch.device("cpu")):

    # Open the TIFF files and extract the data as NumPy arrays
    with rasterio.open(red) as src:
        redt = src.read(1)

    with rasterio.open(nir) as src:
        nirt = src.read(1)

    with rasterio.open(swir) as src:
        swirt = src.read(1)

    # Combine the NumPy arrays for the different bands into a single NumPy array

    data = np.dstack((redt, nirt, swirt))
    # data[:,:,1].shape
    float_array = data.astype(np.float32)
    # float_array = float_array[:-5400, :-5400]

    input_tensor_test = torch.from_numpy(float_array)
    # print(input_tensor_test.shape)
    tensor_2d = input_tensor_test.reshape(-1, 3)

    # Print the shape of the reshaped tensor
    # print(tensor_2d)

    scaler = MinMaxScaler()
    X2 = scaler.fit_transform(tensor_2d)

    # Move data to CPU
    X2 = torch.Tensor(X2).to(device)

    input_dim = 3
    output_dim = 10
    hidden_dim = 64
    num_layers = 1

    model = EncoderDecoderLSTM(input_dim, hidden_dim, num_layers, output_dim)
    # Load the state_dict
    model.load_state_dict(torch.load('./main_cpu2.pt'))

    # Move the model to the device
    model = model.to(device)

    # Set the model to evaluation mode
    model.eval()

    # Predict
    with torch.no_grad():
        output_tensor = model.forward(X2)
    argmax_tensor = torch.argmax(output_tensor, dim=1)
    # print('argmax_tensor shape = ', argmax_tensor.shape)

    # Convert to numpy
    tensor_cpu = argmax_tensor.cpu()
    argmax_array = tensor_cpu.numpy()

    # print('array_2d', (argmax_array))
    mode = stats.mode(argmax_array, keepdims=True)
    return int(mode[0])
