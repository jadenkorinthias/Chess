import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset
import chess
import numpy as np
from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint
import csv
from pytorch_lightning.loggers import TensorBoardLogger

# Neural network for evaluating chess positions
class ChessNet(pl.LightningModule):
    def __init__(self):
        super(ChessNet, self).__init__()
        self.layer1 = nn.Linear(808, 512)
        self.dropout1 = nn.Dropout(0.1)
        self.layer2 = nn.Linear(512, 256)
        self.dropout2 = nn.Dropout(0.1)
        self.layer3 = nn.Linear(256, 64)
        self.output_layer = nn.Linear(64, 1)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = self.dropout1(x)
        x = F.relu(self.layer2(x))
        x = self.dropout2(x)
        x = F.relu(self.layer3(x))
        return self.output_layer(x)

    def training_step(self, batch, batch_idx):
        positions, evaluations = batch
        evaluations_pred = self(positions)
        loss = F.mse_loss(evaluations_pred, evaluations)
        self.log('train_loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
        return [optimizer], [lr_scheduler]

# Dataset class for handling chess data
class ChessDataset(Dataset):
    def __init__(self, game_records):
        self.game_records = game_records

    def __len__(self):
        return len(self.game_records)

    def __getitem__(self, idx):
        fen, eval = self.game_records[idx]
        board = chess.Board(fen)
        input_vector = self.board_to_input(board)
        return torch.tensor(input_vector, dtype=torch.float32), torch.tensor([eval], dtype=torch.float32)

    @staticmethod
    def board_to_input(board):
        piece_map = board.piece_map()
        input_vector = np.zeros(808, dtype=int)
        for i in range(64):
            piece = piece_map.get(i, None)
            if piece:
                index = i * 12 + piece.piece_type - 1 + (6 if piece.color == chess.BLACK else 0)
                input_vector[index] = 1
        return input_vector

def load_game_records(filename):
    game_records = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            fen, evaluation = row[0], float(row[1])
            game_records.append((fen, evaluation))
    return game_records


def train_model():
    # Load game records from a CSV file
    game_records = load_game_records('lichess_db_standard_rated_2013-01.pgn.zst.csv')  # Ensure the file name is correct
    dataset = ChessDataset(game_records)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Initialize the model
    model = ChessNet()

    # Setup TensorBoard logger
    logger = TensorBoardLogger("tb_logs", name="Chess AI Log")

    # Initialize the Trainer with accelerator for GPU support if available, learning rate monitor, model checkpointing, and TensorBoard logging
    if torch.cuda.is_available():
        accelerator = "ddp"
    else:
        accelerator = "cpu"
    
    trainer = pl.Trainer(
        max_epochs=10, 
        accelerator=accelerator, 
        callbacks=[
            LearningRateMonitor(logging_interval='step'), 
            ModelCheckpoint(dirpath='./model/', every_n_epochs=1)
        ],
        logger=logger  # Pass the logger here
    )
    
    # Train the model
    trainer.fit(model, loader)

if __name__ == '__main__':
    train_model()