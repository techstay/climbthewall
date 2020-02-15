#! /bin/bash

function check_arguments() {
  if [ $# -ne 3 ] && [ $# -ne 2 ]; then
    echo '脚本需要两个或三个参数，两个参数创建ss，三个参数创建ss+kcp，第一个参数是密码，第二个参数是端口号，第三个参数是kcp模式'
    exit 1
  fi
}

function prepare_variables() {
  password="$1"
  port="$2"
  mode="$3"

  interface=$(ip -o -4 route show to default | awk '{print $5}')
  ip=$(ip -4 addr show "$interface" | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

  kcp_dir=".gost_ss"
  mkdir -p "$HOME/$kcp_dir"
  kcp_file="kcp-$port.json"
  kcp_full_path="$HOME/$kcp_dir/$kcp_file"

  if [ $# -eq 2 ]; then
    ss_config="ss://$(echo chacha20-ietf-poly1305:"$password" | base64)@$ip:$port"
  else
    ss_config="ss://$(echo chacha20-ietf-poly1305:"$password" | base64)@$ip:$port/?plugin=kcptun;mode=$mode"
  fi
}

function run_docker_commands() {
  if [ $# -eq 2 ]; then
    sudo docker run --name "gost$port" -d \
      --net=host \
      --restart=always \
      ginuerzh/gost \
      -L="ss2://AEAD_CHACHA20_POLY1305:$password@:$port"
  else
    cat >"$kcp_full_path" <<EOL
{
    "key": "it's a secrect",
    "crypt": "aes",
    "mode": "$mode",
    "mtu": 1350,
    "sndwnd": 1024,
    "rcvwnd": 1024,
    "datashard": 10,
    "parityshard": 3,
    "dscp": 0,
    "nocomp": false,
    "acknodelay": false,
    "nodelay": 0,
    "interval": 40,
    "resend": 0,
    "nc": 0,
    "sockbuf": 4194304,
    "keepalive": 10,
    "snmplog": "",
    "snmpperiod": 60,
    "tcp": false
}
EOL

    sudo docker run --name "gost$port" -d \
      --net=host \
      --restart=always \
      -v "$kcp_full_path":/kcp.json \
      ginuerzh/gost \
      -L="ss2+kcp://AEAD_CHACHA20_POLY1305:$password@:$port?c=/kcp.json"
  fi
}

function print_config() {
  if [ $# -eq 2 ]; then

    echo '-----------以下是shadowsocks客户端配置文件-------------'
    cat <<EOL
{
    "server":["$ip"],
    "server_port":$port,
    "local_port":10800,
    "password":"$password",
    "timeout":60,
    "method":"chacha20-ietf-poly1305",
}
EOL

    echo '-----------以下是gost客户端配置命令-------------'
    cat <<EOL
sudo docker run -d --name gostproxy \
  --restart=always --net=host \
  ginuerzh/gost -L=:10800 \
  '-F=ss2://AEAD_CHACHA20_POLY1305:$password@$ip:$port'
EOL

  else
    echo '-----------以下是gost客户端配置命令-------------'
    cat <<EOLL
mkdir -p ~/"$kcp_dir"
cat >~/"$kcp_dir/$kcp_file" <<EOL
{
    "key": "it's a secrect",
    "crypt": "aes",
    "mode": "$mode",
    "mtu": 1350,
    "sndwnd": 1024,
    "rcvwnd": 1024,
    "datashard": 10,
    "parityshard": 3,
    "dscp": 0,
    "nocomp": false,
    "acknodelay": false,
    "nodelay": 0,
    "interval": 40,
    "resend": 0,
    "nc": 0,
    "sockbuf": 4194304,
    "keepalive": 10,
    "snmplog": "",
    "snmpperiod": 60,
    "tcp": false
}
EOL

sudo docker run -d --name gostproxy \
  --restart=always --net=host \
  -v ~/"$kcp_dir/$kcp_file":/kcp.json \
  ginuerzh/gost -L=:10800 \
  '-F=ss2+kcp://AEAD_CHACHA20_POLY1305:$password@$ip:$port?c=/kcp.json'
EOLL
  fi
  echo '-----------以下是shadowsocks配置字符串,可复制到手机端使用-------------'
  echo "$ss_config"
}

function main() {
  check_arguments "$@"
  prepare_variables "$@"
  run_docker_commands "$@"
  print_config "$@"
}

main "$@"
