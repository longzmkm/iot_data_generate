# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import logging
import socket
import json

logger = logging.getLogger('basement:iot')
logger.setLevel(logging.INFO)


class TCPRequest(object):
    socket = None
    bufsize = 1024

    def __init__(self, host, port, secret_key, **kwargs):
        self.host = host
        self.port = port
        self.secret_key = secret_key
        self.timeout = kwargs.get('timeout', 60)

    def __enter__(self):
        socket.setdefaulttimeout(60)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 维持心跳
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # 设置IP 端口
        self.socket.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send_data(self, payload):
        json_data = json.dumps(payload, sort_keys=False, indent=2)
        self.socket.sendall(json_data)
        data = self.socket.recv(1024)
        return data

    def receive_data(self):
        res = self.socket.recv(self.bufsize)
        return res


if __name__ == '__main__':
    host = "ndp.nlecloud.com"
    port = 8600
    secret_key = 'dd437b7168c34271b21b54ae243df9c3'

    with TCPRequest(host=host, port=port, secret_key=secret_key) as t:
        data = {
            "t": 1,
            "device": "gateway_1",
            "key": "dd437b7168c34271b21b54ae243df9c3",
            "ver": "V1.0"
        }
        res = t.send_data(payload=data)
        print res
        data = {
            "t": 3,
            "msgid": 2,
            "datatype": 1,
            "datas": {
                "nl_temperature": "27"
            }
        }
        res = t.send_data(payload=data)
        print res
