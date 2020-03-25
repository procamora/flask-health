# flask-health


This project is to deploy a container that mounts a REST API to send HTTP POST requests to. The purpose for which it has been designed is to mount it on different segments of the network and from a Controller check that you have access to each of the segments.


# Installation


We can create the container image locally or use the image uploaded to DockerHub. To create the container locally and run it, we can run the following commands:
```bash
docker build -t healthy .
docker run -p8888:8888 --rm healthy
```

To use the DockerHub image we can use the following command:

```bash
docker pull procamora/healthy
```
