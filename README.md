# xenon-rse2017-tutorial

Material for [Xenon](http://nlesc.github.io/Xenon/) tutorial for [Research Software Engineers Conference 2017](http://rse.ac.uk/conf2017/).

## Installation

Requires a virtual machine with minimally 2 cpus.

Step to install tutorial material into the tutorial virtual machine.

```bash
# Login as tutorial user
cd xenon
git clone https://github.com/NLeSC/xenon-rse2017-tutorial.git .
./install.sh
# Enter sudo password when asked
```

After which 
* the [Xenon cli](https://github.com/NLeSC/xenon-cli) has been installed as `~/xenon/xenon-cli/bin/xenon` and added to the PATH env var
* Docker has been installed with SSH, SFTP, Webdav and Slurm enabled images.

### Test

If the install was run in same shell run following to update the users groups and refresh the PATH env var:
```
newgrp docker
```

To SFTP docker image can be started with:

```
docker run --detach --publish 3322:22 nlesc/xenon-ssh
# wait until the container is up and healty by running
docker ps
```

To test if the Xenon-CLI work and can access the container container use: 

```
xenon filesystem sftp --username xenon --password javagat --location localhost:3322 list /home/xenon
```

The Webdav docker image can be started with:

```
docker run --detach --publish 2280:80 nlesc/xenon-webdav
# wait until the container is up and healty by running
docker ps
```

The Webdav server can be tested with:

```
xenon filesystem webdav --username xenon --password javagat --location http://localhost:2280 list ~xenon
```

The Slurm batch scheduler can be started with:

```
docker run --detach --publish 2222:22 nlesc/xenon-slurm:17
# wait until the container is up and healty by running
docker ps
```

To test if the Xenon CLI can access Slurm run:

```
xenon scheduler slurm --username xenon --password javagat --location localhost:2222 exec sinfo
```





