# Running and managing Docker containers

Docker is a software platform that simplifies the process of building, running, managing and distributing applications. It packages applications as **images** that contain everything needed to run them: code, runtime environment, libraries, and configuration. Images run in **containers**, which are discrete processes that take up only as many resources as any other executable.

Docker has been set up for each user of the DGX and _all workloads must be executed through Docker containers._

**_Note_**: This section will _not_ cover how to build your own Docker image. Instead, we will use an image that I prepared beforehand.

___
### Download (or build) a Docker image
In order to run the code in this tutorial, we will use a Docker image hosted on DockerHub.

We will utilise the command `docker pull` to fetch it:

```bash
docker pull rbonazzola/learn_workshop:session_2
```

Alternatively, you can build the same Docker image yourself (it will take longer). The source `Dockerfile` is called `docker/Dockerfile_pt113_cu117_ptl19`.

To do this, run the following command from the `LEARN_workshop/docker` directory: 

```bash
docker build -f Dockerfile_pt113_cu117_ptl19 -t rbonazzola/learn_workshop:session_2 .
``` 

(don't forget the dot in the end).

In this case, the _name_ of the image is `rbonazzola/learn_workshop` and the _tag_ is `session_2`.

___
### Examine the Docker images
To examine the Docker images available locally, run

```bash
docker image ls
```

This will output a table with the different images, including their name and tag, their ID (a hexadecimal string) and the size.

### Run a container
You can run containers in two ways: batch mode and interactive mode. In this tutorial, we will mostly use interactive mode.

To run a container in interactive mode, add the `-it` option.
```bash
docker run -it rbonazzola/learn_workshop:session_2
```

If we wanted to execute a second shell from _the same container_, we can `docker ps` to see this container's ID, then do

```bash
docker exec -it <CONTAINER_ID> bash
```

(`docker run` launches a new container, `docker exec` executes a command in a container that is already running.)

To quit the container, you can use `ctrl+D` or run `exit`. This will _stop_ the container but will not _kill_ it, as you can see by running `docker ps -a`.

If you want the container to be killed automatically after you exit it, use `docker run` with the `--rm` option.

In the following, we will make the `docker run` increasingly complex by adding more options.

#### Request (CPU) memory

```bash
docker run -it --shm-size=32gb rbonazzola/learn_workshop:session_2
```

#### Mounting a volume
Add the `--mount` option, and specify the source (host's) and target (container's) paths.

```bash
docker run -it --mount type=bind,source=${SOURCEPATH},target=${TARGETPATH} rbonazzola/learn_workshop:session_2
```

#### Mapping ports
This command will map port 1234 in the container to port 5678 in the host (note the order).

```bash
docker run -it --shm-size=32gb -p 5678:1234 rbonazzola/learn_workshop:session_2
```

#### Request a GPU or MIG device
When utilising GPU resources, note that the container does not contain the GPU drivers. Instead, this belong to the host and must be made "visible" to the container by adding the `--gpus` option.

The following command will request the MIG device 0 within GPU 1 (`1:0`):

```bash
docker run -it --gpus '"device=1:0"' --shm-size=32gb -p 5678:1234 rbonazzola/learn_workshop:session_2
```

#### Full command

```bash
DEVICE="1:0" # change by another device. This stands for GPU_ID:MIG_ID.
SOURCEPATH="${HOME}/LEARN_workshop" # if you didn't clone the repo in the home dir, change accordingly
TARGETPATH="/root/LEARN_workshop"
PORT=13467 # change by another random port >10000, and remember this port for the SSH tunneling

#You can use the following command without changes if you've set up the above variables
docker run -it -p ${PORT}:8888 --shm-size=32gb --gpus '"device='$DEVICE'"' --user root --mount type=bind,source=${SOURCEPATH},target=${TARGETPATH} rbonazzola/learn_workshop:session_2
```

### Additional options
You can explore the help from the different Docker subcommands by running `docker <SUBCOMMAND> --help`, e.g. `docker run --help` or `docker build --help`.
Likewise, you can list the different subcommands by running `docker --help`.
