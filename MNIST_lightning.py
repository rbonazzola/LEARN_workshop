import pytorch_lightning as pl
from typing import Union, List
from torch.utils.data import TensorDataset, DataLoader, random_split
import torch
from IPython import embed

class MNIST_DataModule(pl.LightningDataModule):

    def __init__(self, 
          batch_size:int = 32,
          split_lengths: Union[None, List[int]] = None,
        ):

        super().__init__()

        self.batch_size = batch_size
        self.split_lengths = split_lengths


    def setup(self, stage):
        from torchvision import datasets
        from torchvision import transforms

        mnist_trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transforms.Compose([transforms.ToTensor()]))
        mnist_testset = datasets.MNIST(root='./data', train=False, download=True, transform=transforms.Compose([transforms.ToTensor()]))

        self.train_dataset, self.val_dataset = random_split(mnist_trainset, self.split_lengths)
        self.test_dataset = mnist_testset 


    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, num_workers=8)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=8)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=8)


        


class CNN_Module(pl.LightningModule):

    def __init__(self, model):

        super().__init__()

        self.model = model
        self.ce_loss = torch.nn.CrossEntropyLoss()
        
        self.training_step_outputs = []
        self.validation_step_outputs = []
        self.test_step_outputs = []


    def forward(self, input: torch.Tensor, **kwargs) -> torch.Tensor:
        return self.model(input, **kwargs)


    def training_step(self, batch, batch_idx):
    
        image, label = batch
        pred = self.model(image)
        loss = self.ce_loss(pred, label)

        loss_dict = { "loss": loss }

        self.training_step_outputs.append(loss_dict)
        
        self.log_dict(loss_dict)
        
        return loss_dict
    
    
    def on_train_epoch_end(self):
        
        outputs = self.training_step_outputs

        avg_loss = torch.stack([x["loss"] for x in outputs]).mean() 
        self.log_dict({
            "training_loss": avg_loss
          },
          on_epoch=True,
          prog_bar=True,
          logger=True,
        )
        self.training_step_outputs.clear()
    
    
    def validation_step(self, batch, batch_idx):

        image, label = batch
        pred = self.model(image)
        loss = self.ce_loss(pred, label)
   
        accuracy = (label == pred.argmax(axis=1)).sum() / len(pred)
        loss_dict = { 
          "loss": loss,
          "accuracy": accuracy
        }

        self.validation_step_outputs.append(loss_dict)
        self.log_dict(loss_dict)
        return loss_dict

    
    
    def on_validation_epoch_end(self):
    
        outputs = self.validation_step_outputs
        avg_loss = torch.stack([x["loss"] for x in outputs]).mean() 
        accuracy = torch.stack([x["accuracy"] for x in outputs]).mean() 
        self.log_dict({
            "val_loss": avg_loss,
            "val_accuracy": accuracy
          },
          on_epoch=True,
          prog_bar=True,
          logger=True,
        )
        self.validation_step_outputs.clear()
    
    
    def test_step(self, batch, batch_idx):
    
        image, label = batch
        pred = self.model(image)
        loss = self.ce_loss(pred, label)

        accuracy = (label == pred.argmax(axis=1)).sum() / len(pred)
        loss_dict = { 
            "loss": loss,
            "accuracy": accuracy
        }
        
        self.test_step_outputs.append(loss_dict)

        self.log_dict(loss_dict)
        return loss_dict



    def on_test_epoch_end(self):

        outputs = self.test_step_outputs
        avg_loss = torch.stack([x["loss"] for x in outputs]).mean()
        accuracy = torch.stack([x["accuracy"] for x in outputs]).mean() 
        self.log_dict({
            "test_loss": avg_loss,
            "test_accuracy": accuracy
          },
          on_epoch=True,
          prog_bar=True,
          logger=True,
        )
        self.test_step_outputs.clear()



    def configure_optimizers(self):

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.0001, betas=[0.5, 0.99], weight_decay=0.0005)
        return optimizer
