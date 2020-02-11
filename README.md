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
