import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import matplotlib.pyplot as plt

class InventoryDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        image = self.data[idx]
        label = self.labels[idx]
        return {'data': torch.tensor(image, dtype=torch.float), 'label': torch.tensor(label, dtype=torch.long)}

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train(model, device, loader, optimizer, criterion):
    model.train()
    loss_val = []
    for batch_idx, (data, target) in enumerate(loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        loss_val.append(loss.item())
    return np.array(loss_val)

def test(model, device, loader, criterion):
    model.eval()
    loss_val = []
    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(loader):
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            loss_val.append(loss.item())
    return np.array(loss_val)

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    labels = np.array([0, 1, 2])
    dataset = InventoryDataset(data, labels)
    batch_size = 32
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    
    model = CNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    
    epochs = 10
    for epoch in range(epochs):
        print('Epoch:', epoch + 1)
        loss = train(model, device, train_loader, optimizer, criterion)
        test_loss = test(model, device, train_loader, criterion)
        plt.plot(loss, label='Training Loss')
        plt.plot(test_loss, label='Test Loss')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main()