import pytorch_lightning as ptl
import mlflow
from MNIST_example.MNIST import MNISTClassifier
from MNIST_lightning import CNN_Module, MNIST_DataModule 
from my_ptl_callbacks import early_stopping, model_checkpoint, progress_bar, rich_model_summary


if __name__ == "__main__:

    mlflow.set_tracking_uri(uri)
    
    try:
        exp_id = mlflow.create_experiment(exp_name)
    except:
        # If the experiment already exists, we can just retrieve its ID
        exp_id = mlflow.get_experiment_by_name(exp_name).experiment_id
    
    mlflow.pytorch.autolog(log_models=False)
    
    callbacks = [ early_stopping, model_checkpoint, progress_bar, rich_model_summary ]

    import argparse
    
    parser = argparse.ArgumentParser("MNIST training")
    parser.add_argument("--batch_size", default=512)
    parser.add_argument("--precision", default="16")
    
    args = parser.parse_args()

    mlflow.log_parameters({"precision": args.precision})
    
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