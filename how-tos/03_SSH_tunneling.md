# SSH tunneling
If we want to use e.g. a web interface for a service running on a container, we will need to do SSH tunneling (also known as _port forwarding_).

### On Unix-like systems

```bash
ssh -L LOCAL_PORT:DESTINATION:DESTINATION_PORT your_user@cistib-dgx01.leeds.ac.uk
```

For example:

```bash
ssh -L 8888:localhost:8888 your_user@cistib-dgx01.leeds.ac.uk
```

You can access this web interface by typing `localhost:8888` in the address bar.

### On MobaXterm (Windows)
Press the **Tunneling** button, and add a new SSH tunnel (using "Local port forwarding").
![](../figures/local-port-forwarding.png)
