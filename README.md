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

利用gost工具生成影梭和kcp的服务端工具。

首先确保你已经安装并启动了docker服务。

```shell script
# Ubuntu 18.04
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

然后下载`gost_ss.sh`脚本并运行，该脚本需要两个或三个参数，前两个参数分别是影梭的密码和端口号；第三个参数是kcp的mode，不指定的话启动影梭，指定了的话使用影梭+kcp。mode的可选值有fast,fast2和fast3，如果是自用的VPS而且流量充足，直接指定fast3来获得最高的加速效果。

```shell script
wget https://raw.githubusercontent.com/techstay/climbthewall/master/gost_ss.sh
# 启动影梭服务，脚本会显示相应的客户端配置文件，请记下来
bash gost_ss.sh 123456 10086
# 启动影梭和kcp加速，客户端需要安装kcp
bash gost_ss.sh 123456 10086 fast3
```

