### Building your own Docker image

There are two ways of doing this:

    - Create a Dockerfile.
    - Modify an existing image interactively and committing the changes.
    
### Dockerfile

Once you have a Dockerfile ready, you can build an image from it running the following command:

```bash
docker build -f <DOCKERFILE_LOCATION> -t <IMAGE_NAME> .
```

Now we will see how to create a Dockerfile. You can use the one located in this repository under `docker/Dockerfile` as a reference for your own project.

**Choose your base image**

```Dockerfile
FROM <BASE_IMAGE>
```

e.g.
```Dockerfile
FROM ubuntu:latest
```

**Install libraries (assuming Ubuntu)**

```Dockerfile
RUN apt-get update 
RUN apt-get install -y \
    curl \
    ca-certificates \
    vim \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    wget \
    zip tar unzip \
    gcc \
    tmux \
    make \
 && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install -y --reinstall build-essential
RUN apt-get install -y libboost-dev
```

**Set up a non-root user**

```Dockerfile
# Create a non-root user and switch to it.
RUN adduser --disabled-password --gecos '' --shell /bin/bash user
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory.
ENV HOME=/home/user
RUN chmod 777 /home/user
```

**Set up a Conda environment**

```Dockerfile
RUN curl -so ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Create e.g. a Python 3.9 environment.
RUN /home/user/miniconda/bin/conda install conda-build
RUN /home/user/miniconda/bin/conda create -y --name <ENV_NAME> python=3.9
RUN /home/user/miniconda/bin/conda clean -ya

ENV CONDA_DEFAULT_ENV=<ENV_NAME>
ENV CONDA_PREFIX=/home/user/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH

ENV TORCH=1.10
ENV CUDA=cu113
RUN conda install pytorch=${TORCH} torchvision torchaudio cudatoolkit=11.3 -c pytorch
RUN conda install tqdm -c conda-forge
RUN conda install jupyter -c anaconda
RUN conda install pytorch-lightning -c conda-forge
RUN conda install mlflow==1.23 -c conda-forge
```

**_Note:_** ARC3, ARC4, Bede and JADE have Singularity installed, however a Docker image can be run from Singularity. Therefore, if you choose carefully the libraries's versions on your Docker images (such that they are compatible with the Nvidia drivers installed), in principle you could readily use this image on those platforms.

```bash
singularity build <SINGULARITY_IMAGE_NAME>.sif docker-daemon://<DOCKER_IMAGE_NAME>:<TAG>
```
