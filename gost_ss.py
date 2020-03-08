#! /usr/bin/env python

import argparse
import subprocess
import pathlib
import urllib.request
import secrets
import string
import base64
import json
import socket


class SystemUtils:
    @staticmethod
    def create_file(fullpath, filecontent):
        file = pathlib.Path(fullpath).resolve().expanduser()
        parentdir = file.parent
        if not parentdir.exists():
            parentdir.mkdir(parents=True, exist_ok=True)
        file.write_text(filecontent)
        return file

    @staticmethod
    def test_command_exist(command):
        exist = True
        try:
            subprocess.run(rf'which {command}', shell=True, check=True)
        except subprocess.CalledProcessError:
            exist = False
        return exist

    @staticmethod
    def get_local_ip():
        request = urllib.request.Request('http://httpbin.org/ip')
        response = urllib.request.urlopen(request)
        ip = json.loads(response.read().decode())['origin']
        socket.inet_aton(ip)
        return ip


class RandomUtils:
    """Generate random passwords and ports"""

    @staticmethod
    def get_rand_passwords(length=12):
        pool = string.ascii_letters + string.digits
        return ''.join(secrets.choice(pool) for _ in range(length))

    @staticmethod
    def get_random_port():
        """Get an unused port"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]


class DockerUtils:
    @staticmethod
    def run_gost_ss(password, port):
        try:
            subprocess.run(
                rf'docker run --name gost{port} -d --net=host --restart=always ginuerzh/gost -L=ss://AEAD_CHACHA20_POLY1305:{password}@:{port} '
                    .split(' '), check=True, stderr=subprocess.STDOUT)
            print('----------以下是shadowsocks-libev客户端配置文件----------')
            print(rf'''
{{
    "server":["{SystemUtils.get_local_ip()}"],
    "server_port":{port},
    "local_port":10800,
    "password":"{password}",
    "timeout":60,
    "method":"chacha20-ietf-poly1305",
}}
''')
            print('-------------以下是docker gost客户端配置命令---------------')
            print(rf'''
docker run -d --name gostproxy \
  --restart=always --net=host \
  ginuerzh/gost -L=:10800 \
  '-F=ss://AEAD_CHACHA20_POLY1305:{password}@{SystemUtils.get_local_ip()}:{port}'
''')

            print('---------------以下是shadowsocks配置字符串，可用于手机端等------------------')
            userinfo = base64.urlsafe_b64encode(rf'chacha20-ietf-poly1305:{password}'.encode('utf8')).decode('utf8')
            print(rf'ss://{userinfo}@{SystemUtils.get_local_ip()}:{port}')
        except subprocess.CalledProcessError as e:
            print(e.output)

    @staticmethod
    def run_gost_ss_kcp(password, port, mode):
        kcp_file = rf'~/.gost_ss/kcp{port}.json'
        kcp_config = rf'''
{{
    "key": "it's a secrect",
    "crypt": "aes",
    "mode": "{mode}",
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
}}'''

        kcp_file_path = str(SystemUtils.create_file(kcp_file, kcp_config))
        try:
            subprocess.run(
                rf'docker run --name gost{port} -d --net=host --restart=always -v {kcp_file_path}:/kcp.json '
                rf'ginuerzh/gost -L=ss+kcp://AEAD_CHACHA20_POLY1305:{password}@:{port}?c=/kcp.json'
                    .split(' '), check=True, stderr=subprocess.STDOUT)

            print('-------------以下是docker gost客户端配置命令---------------')
            print(rf'''
mkdir -p ~/.kcp/
tee ~/.kcp/kcp{port}.json <<EOL
{{
    "key": "it's a secrect",
    "crypt": "aes",
    "mode": "{mode}",
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
}}
EOL
docker run -d --name gostproxy \
  --restart=always --net=host \
  -v ~/.kcp/kcp{port}.json:/kcp.json \
  ginuerzh/gost -L=:10800 \
  '-F=ss+kcp://AEAD_CHACHA20_POLY1305:{password}@{SystemUtils.get_local_ip()}:{port}?c=/kcp.json'
''')

            print('---------------以下是shadowsocks配置字符串，可用于手机端等------------------')
            userinfo = base64.urlsafe_b64encode(rf'chacha20-ietf-poly1305:{password}'.encode('utf8')).decode('utf8')
            print(rf'ss://{userinfo}@{SystemUtils.get_local_ip()}:{port}/?plugin=kcptun;mode={mode}')
        except subprocess.CalledProcessError as e:
            print(e.output)


class GostSs:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-password', default=RandomUtils.get_rand_passwords(),
                                 help='密码，未指定则使用随机密码')
        self.parser.add_argument('-port', default=RandomUtils.get_random_port(),
                                 help='端口号，未指定则使用随机端口号')
        group = self.parser.add_argument_group('kcp')

        group.add_argument('-k', dest='kcp', action='store_true', help='是否使用kcp协议加速')
        group.add_argument('-mode', choices=['fast', 'fast2', 'fast3'], default='fast',
                           help='kcp协议的加速模式，流量充足可使用fast3')

    def run(self):
        args = self.parser.parse_args()
        if args.kcp:
            DockerUtils.run_gost_ss_kcp(args.password, args.port, args.mode)
        else:
            DockerUtils.run_gost_ss(args.password, args.port)


if __name__ == '__main__':
    progs = GostSs()
    progs.run()
