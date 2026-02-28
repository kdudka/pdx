# Installation steps specific for Gentoo Linux

## Install podman

- make sure kernel is compiled with:
```
CONFIG_CGROUPS=y
CONFIG_CGROUP_PIDS=y
CONFIG_MEMCG=y
CONFIG_USER_NS=y
```

- install the user-space for podman:

```sh
emerge -av app-containers/podman
```

- configure UID/GID ranges (replace `kdudka` by your own user):

```sh
echo kdudka:100000:65536 | tee -a /etc/sub{u,g}id
```

## Install packages for HW acceleration (optional)

```sh
emerge -av dev-util/nvidia-cuda-toolkit sci-ml/pytorch sci-ml/torchvision sys-process/nvtop x11-drivers/nvidia-drivers
```
