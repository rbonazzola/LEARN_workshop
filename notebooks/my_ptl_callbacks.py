from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks import RichProgressBar
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks.progress.rich_progress import RichProgressBarTheme
from pytorch_lightning.callbacks import RichModelSummary

early_stopping = EarlyStopping(monitor="val_loss", mode="min", patience=3)

model_checkpoint = ModelCheckpoint(monitor='val_loss', save_top_k=1)

rich_model_summary = RichModelSummary(max_depth=-1)

progress_bar = RichProgressBar(
  theme=RichProgressBarTheme(
    description="green_yellow",
    progress_bar="green1",
    progress_bar_finished="green1",
    progress_bar_pulse="#6206E0",
    batch_progress="green_yellow",
    time="grey82",
    processing_speed="grey82",
    metrics="grey82",
  )
)