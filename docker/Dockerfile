FROM ubuntu:latest

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
RUN apt-get install lsb-release -y


# Create a non-root user and switch to it.
RUN adduser --disabled-password --gecos '' --shell /bin/bash user
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory.
ENV HOME=/home/user
RUN chmod 777 /home/user

# Install Miniconda
RUN curl -so ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Create e.g. a Python 3.9 environment.
RUN /home/user/miniconda/bin/conda install conda-build
RUN /home/user/miniconda/bin/conda create -y --name pytorch_test python=3.9
RUN /home/user/miniconda/bin/conda clean -ya

ENV CONDA_DEFAULT_ENV=pytorch_test
ENV CONDA_PREFIX=/home/user/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH

ENV TORCH=1.10
ENV CUDA=cu113
RUN conda install pytorch=${TORCH} torchvision torchaudio cudatoolkit=11.3 -c pytorch
RUN conda install tqdm -c conda-forge
RUN conda install jupyter -c anaconda
RUN conda install pytorch-lightning -c conda-forge
# RUN conda install mlflow==1.23 -c conda-forge
