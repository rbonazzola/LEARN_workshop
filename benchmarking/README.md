# Benchmarking
In this section, we'll see how to leverage what we have done so far on Docker, to be able to run our code on other platforms, namely ARC and JADE2. This will allow us to do some benchmarking against the DGX A100 platform.

## Singularity
Both ARC and JADE2 provide Singularity as containerisation technology.
Fortunately, Singularity images can be easily generated from the corresponding Docker images.

To do this, you can execute, e.g.

```singularity pull $HOME/singularity_images/myUbuntu.sif docker://ubuntu:latest```

This will create a file called `$HOME/singularity_images/myUbuntu.sif` based on the image `ubuntu:latest` hosted on DockerHub.

**Tip:** add a line `export SIF_FOLDER=$HOME/singularity_images` (change by another location if needed) to your `~/.bashrc` or `~/.bash_profile` script, and save all your .sif files in that location.

## ARC3 and ARC4
*Note:* Take into account the Nvidia drivers' versions installed in each of the GPU nodes, when deciding which DL library to install in your image. At this moment (12-05-2023) these versions were:
- ARC3 K80 nodes: 460.73.01, CUDA version: 11.2.
- ARC3 P100 nodes: 525.85.12, CUDA Version: 12.0.
- ARC4 V100 nodes: ???

```
SOURCE_FOLDER=...
TARGET_FOLDER=...
SIF=${SIF_FOLDER}/...
CMD=...

module load singularity

singularity exec \
--bind $SOURCE_FOLDER:$TARGET_FOLDER \
--env ENVVAR1=$ENVVAR1 \
--env ENVVAR2=$ENVVAR2 \
$SIF \
sh -c "$CMD"
```

## JADE2
See the [Docs](https://docs.jade.ac.uk/en/latest/jade/containers.html#singularity-containers).
  
Importantly, your image must contain two folders, `/tmp` and `/local_scratch`.
