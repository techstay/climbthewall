# climbthewall

你懂的

## wireguard

一个简易的wireguard配置脚本，使用前请确保系统已经安装好wireguard，并可以使用wg命令。如果已经存在`/etc/wireguard/wg0.conf`文件，或者已经使用`wg-quick up wg0`命令，请删除配置文件，并使用`wg-quick down wg0`关闭wg0，然后再运行本脚本。

### 安装wireguard

首先安装wireguard：

```sh
# Ubuntu 19.10及更新的系统
$ sudo apt install wireguard

# Ubuntu 19.04及更旧的系统
$ sudo add-apt-repository ppa:wireguard/wireguard
$ sudo apt-get update
$ sudo apt-get install wireguard

# 如果系统提示未找到add-apt-repository命令
# 请先安装software-properties-common
# 然后再运行add-apt-repository命令
$ sudo apt-get install software-properties-common
```

其他系统安装请查看wireguard官方安装教程。

### 运行脚本

下载脚本，运行即可。密钥对及配置文件保存在`~/.wireguard/`下。

```sh
wget https://raw.githubusercontent.com/techstay/climbthewall/master/wg.sh
bash wg.sh
```

### 使用客户端连接

到[wireguard官网](https://www.wireguard.com/install/)下载客户端，将上面生成的客户端配置文件保存，导入客户端即可。

手机客户端使用时，可以从`client.conf`生成二维码。

```sh
# 使用Python生成二维码，首先安装qrcode
pip install qrcode[pil]

# 生成二维码
cat client.conf|qr > client.png
```

## gost_ss

利用gost工具生成影梭和kcp的服务端脚本。

首先确保你已经安装并启动了docker服务。

```shell script
# Ubuntu 18.04
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

脚本直接使用了docker命令，所以为了顺利运行，你还需要允许docker命令以非管理员权限方式来运行。

```shell script
sudo gpasswd docker -a $(whoami)
sudo systemctl restart docker
```

试一试看看能不能直接启动容器，如果可以的话，就可以运行脚本了。

```shell script
docker run --rm hello-world
```

然后下载`gost_ss.py`脚本并运行，该脚本需要Python3环境才能运行。最简单的运行方式是`python gost_ss.py`，如果要使用kcp协议，则还需要添加kcp两个参数，如`python gost_ss.py -k -mode fast3`。kcp协议需要客户端有kcptun插件或者工具，并正确配置。

```shell script
# 下载脚本
wget https://raw.githubusercontent.com/techstay/climbthewall/master/gost_ss.py

# 用python运行脚本
python gost_ss.py -h
usage: gost_ss.py [-h] [-password PASSWORD] [-port PORT] [-k] [-mode {fast,fast2,fast3}]

optional arguments:
  -h, --help            show this help message and exit
  -password PASSWORD    密码，未指定则使用随机密码
  -port PORT            端口号，未指定则使用随机端口号

kcp:
  -k                    是否使用kcp协议加速
  -mode {fast,fast2,fast3}
                        kcp协议的加速模式，流量充足可使用fast3
```

如果脚本成功运行，会显示出对应的客户端配置信息，请妥善保存。如果发现其他问题，可以直接发issue，最好同时提供错误信息方便定位。
