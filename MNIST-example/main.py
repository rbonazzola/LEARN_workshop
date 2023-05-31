import pytorch_lightning as ptl
import mlflow
from MNIST_lightning import CNN_Module, MNIST_DataModule 
from my_ptl_callbacks import early_stopping, model_checkpoint, progress_bar, rich_model_summary

import torch
from torch import nn
import torch.nn.functional as F

class MNISTClassifier(nn.Module):

    def __init__(self):
        super(MNISTClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.softmax(x, dim=1)
        return output


if __name__ == "__main__":


    import argparse
    
    parser = argparse.ArgumentParser("MNIST training")
    parser.add_argument("--batch_size", default=512)
    parser.add_argument("--precision", default="16")
    parser.add_argument("--mlflow_exp_name", default="test")
    
    args = parser.parse_args()
    
    uri = "./mlruns"
    mlflow.set_tracking_uri(uri)
   
    exp_name = args.mlflow_exp_name
    try:
        exp_id = mlflow.create_experiment(exp_name)
    except:
        # If the experiment already exists, we can just retrieve its ID
        exp_id = mlflow.get_experiment_by_name(exp_name).experiment_id
    
    mlflow.pytorch.autolog(log_models=False)
    
    callbacks = [ early_stopping, model_checkpoint, progress_bar, rich_model_summary ]

    mlflow.log_params({"precision": args.precision})
    
    model = MNISTClassifier()
    datamodule = MNIST_DataModule(batch_size=args.batch_size, split_lengths=[48000, 12000])
    ptl_module = CNN_Module(model)
    
    trainer = ptl.Trainer(
        accelerator="gpu",
        devices=1,
        precision=args.precision,
        callbacks=callbacks,
        min_epochs=5
    )
    
    trainer.fit(ptl_module, datamodule)
