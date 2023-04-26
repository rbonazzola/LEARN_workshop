# LEARN workshop
Material for the LEARN workshop on the DGX A100.

## Cloning this repository
Clone this repository by running

```bash
git clone https://github.com/rbonazzola/LEARN_workshop.git
```

## How-to's
The folder `how-tos` contains a series of MD files that will guide you through the process of getting on board of the DGX A100.

- [0 - About the DGX](how-tos/00_About_the_DGX.md).
- [1 - How to access the DGX A100](how-tos/01_How_to_access_the_DGX.md).
- [2 - Running and managing Docker containers](how-tos/02_Running_a_Docker_container.md).
- [3 - SSH tunneling](how-tos/03_SSH_tunneling.md).
- [4 - How to build your own Dockerfile](how-tos/05_How_to_build_your_own_Dockerfile.md).

## Notebooks
The folder `notebooks` contains Jupyter notebooks for previous workshop sessions.

- [Session 1](notebooks/LEARN_workshop_session1.ipynb) explores some features of the DGX A100 useful for deep learning, such as 16-bit precision, using plain PyTorch and also PyTorch Lightning.
- [Session 2](notebooks/LEARN_workshop_session2.ipynb) covers the implementation of a simple DL model (for MNIST digit recognition) using PyTorch Lightning, and also how to log model information using MLflow.
