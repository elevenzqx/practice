---
title: Linux 远程 GUI 显示
cover: https://cdn.pixabay.com/photo/2023/09/25/10/46/krka-8274679_1280.jpg
thumbnail: https://images.pexels.com/photos/1835008/pexels-photo-1835008.jpeg?auto=compress&cs=tinysrgb&w=1600
categories: 
- 环境搭建
tags:
- linux
---

## windowns 使用

Windows 这边需要安装 x11 程序，常见商业软件 Xmanager，免费的 XMing 和 VcXsrv 这里选择微软的开源 VcXsrv

https://sourceforge.net/projects/vcxsrv/

安装后进行简单配置:

* 第一步: 保留默认 Multiple windows 和 Display number -1

* 第二步: 选 start no client

* 第三步: 这一步比较重要，勾选 Disable acccess control

<!--more-->

### WSL 下使用

### docker 下启用

设置启动的环境变量信息

```
docker run -ti --rm -e DISPLAY=host.docker.internal:0.0 firefox
```

或者

```
export DISPLAY=host.docker.internal:0.0
```

拓展说明:

从 18.03 版本开始，Docker 推荐容器使用 host.docker.internal 来访问宿主机上的服务，容器的 DNS 会自动解析到宿主机的内部IP上，

参考 Docker for Windows 的官方文档：

[I WANT TO CONNECT FROM A CONTAINER TO A SERVICE ON THE HOST](https://docs.docker.com/desktop/networking/#use-cases-and-workarounds)

### linux 子系统下

未测试

```
docker run \
-itd \
--net=host \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
--name alpine-firefox \
alpine sh && \
\
docker start alpine-firefox && \
docker exec -it alpine-firefox sh
```

## 测试软件

```
apt install x11-apps
xeyes
```

## macos 使用

* 在 [XQuartz](https://www.xquartz.org/) 下载、安装、运行，当前版本是 2016-10-29 的 2.7.11
* 在 XQuartz 的配置窗口里勾选 「Allow connections from network clients」
* 添加访问控制白名单 xhost + 127.0.0.1，或禁用访问控制 xhost +
* 运行容器并通过DISPLAY环境变量指定X11转发地址 docker run -e DISPLAY=host.docker.internal:0 jess/firefox
