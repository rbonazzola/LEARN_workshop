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

## Dockerfiles
The `docker` folder contains `Dockerfile`'s that you can use as a reference to build your own.

___
## References
**Hardware**
- [DGX A100 white paper](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/dgx-a100/dgxa100-system-architecture-white-paper.pdf)
- [Nvidia A100 Tensor Core GPU paper](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf)

**Multiple Instance GPU (MIG)**
- [MIG user guide from Nvidia](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)

**Docker**
- [Docker basics - how to use Dockerfiles](https://thenewstack.io/docker-basics-how-to-use-dockerfiles/)

**Deep learning training**
- https://sebastianraschka.com/blog/2023/pytorch-faster.html#3-automatic-mixed-precision-training
- https://sebastianraschka.com/blog/2023/pytorch-faster.html#5-training-on-4-gpus-with-distributed-data-parallel
- https://sebastianraschka.com/blog/2023/pytorch-faster.html#6-deepspeed
