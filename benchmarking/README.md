# Benchmarking
In this section, we'll see how to leverage what we have done so far on Docker, to be able to run our code on other platforms, namely ARC and JADE2. This will allow us to do some benchmarking against the DGX A100 platform.

## Singularity
Both ARC and JADE2 provide Singularity as containerisation technology.
Fortunately, Singularity images can be easily generated from the corresponding Docker images, as we'll see below.

___
## ARC3 and ARC4
The queue scheduler on ARC is SGE (Son of Grid Engine).

To create the SIF file from a Docker image hosted on DockerHub, you can execute, e.g.

```
module load singularity
mkdir $HOME/singularity_images # or whichever location you prefer
singularity pull $HOME/singularity_images/myUbuntu.sif docker://ubuntu:latest
```

This will create a file called `$HOME/singularity_images/myUbuntu.sif` based on the image `ubuntu:latest` hosted on DockerHub.

For the Docker image we're using in this workshop, run:

```
singularity pull $HOME/singularity_images/learn.sif docker://rbonazzola/learn_workshop:session_2
```

**Tip:** add a line `export SIF_FOLDER=$HOME/singularity_images` (change by another location if needed) to your `~/.bashrc` or `~/.bash_profile` script, and save all your .sif files in that location.

To submit a job using Singularity, you can write a script like the following, which we will call `launch_singularity_job` (fill in the env variables appropriately):

```
#!/bin/bash
# Your
# SGE header
# comes here

SOURCE_FOLDER=...
TARGET_FOLDER=...
SIF=${SIF_FOLDER}/...
CMD=...

module load singularity

export SINGULARITYENV_CUDA_VISIBLE_DEVICES=0

singularity exec \
--bind $SOURCE_FOLDER:$TARGET_FOLDER \
--nv \
--env ENVVAR1=$ENVVAR1 \
--env ENVVAR2=$ENVVAR2 \
$SIF \
sh -c "$CMD"
```

Then you can submit this job as:

```qsub -v ENVVAR1=... -v ENVVAR2=... -cwd -l h_rt=8:00:00 -l h_vmem=8g launch_singularity_job```

*Note:* Take into account the Nvidia drivers' versions installed in each of the GPU nodes, when deciding which DL library to install in your image. At this moment (12-05-2023) these versions were:
- ARC3 K80 nodes: 460.73.01, CUDA version: 11.2.
- ARC3 P100 nodes: 525.85.12, CUDA Version: 12.0.
- ARC4 V100 nodes: 525.85.12, CUDA Version: 12.0.

___
## JADE2
JADE2 uses Slurm as queue manager. The most important commands to know are `srun`, `sbatch` and `squeue` (or `squeue -u $(whoami)` to status of your own processes).

You can use Docker and Singularity, although the first has many limitations and only containers that are already present on the system can be used. That's why we will focus on Singularity.

Singularity can be used in interactive or batch mode, by means of the commands `/jmain02/apps/singularity/singinteractive` and `/jmain02/apps/singularity/singbatch`, respectively, which are custom JADE wrappers.

Importantly, your image must contain two folders, `/tmp` and `/local_scratch`.

### Singularity in interactive mode
In interactive mode, you can run the following command:
```
srun -I \
--pty \
-t 0-10:00 \
--gres gpu:1 \
--partition=devel \
/jmain02/apps/singularity/singinteractive $SIF
```
where `SIF` env variable contains the path to your SIF image.

### Singularity in batch mode
In batch mode, I've noticed the provided script `singbatch` doesn't work. By examining this script, I noticed there seems to be a misplaced argument in the `singularity exec` command (see [this old issue](https://github.com/jade-hpc-gpu/jade-hpc-gpu.github.io/issues/82) that reports the same problem). Namely, the image name (`$1` argument) should be placed after all the options, and immediately before the script (`$2` argument).
To circumvent this problem, you can just copy this script in some location of yours and modify this line accordingly.
Assuming the new `singbatch` script is placed in your current working directory, you can execute the following command to submit a batch process running Singularity to the Slurm queue:

```
sbatch \
-t 0-10:00 \
--gres gpu:1 \
--partition=devel \
./singbatch $SIF \ 
$SCRIPT
```

`partition` can also be `small` or `big`.
For more information, see the [Docs](https://docs.jade.ac.uk/en/latest/jade/containers.html#singularity-containers). 

*Note 1*: The docs refer to some Singularity images that are supposed to be available on the system under `/jmain02/apps/singularity/singularity-images/`, although I hvaen't been able to find this folder.  

*Note 2*: I have run into errors when requesting GPUs via Singularity. I believe there is a problem in the `singbatch` script .
