# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import hashlib
import logging
import socket
import json
import time
import arrow
import uuid
import paho.mqtt.client as mqtt

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


def on_publish(client, userdata, result):
    print '>>>>' * 50
    print("data published \n")
    pass


def on_connect(data, flags, rc):
    print data, flags, rc


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


class MqttRequest(object):
    """
    host: ndp.nlecloud.com
    prot: 1883
    device_tag: 网关 设备标识
    project_id: 项目ID
    secret_key: SecretKey

    """

    def __init__(self, host, port, device_tag, porject_id, secret_key, **kwargs):

        # Initialize MQTT client.
        self._client = mqtt.Client()  # create MQTT client
        self.host = host
        self.port = port
        self.device_tag = device_tag
        self.project_id = porject_id
        self.secret_key = secret_key

        self._client.on_connect = self._on_connect
        self._connected = False
        self._client.on_publish = self._on_publish

    def jm_sha256_single(self, value):
        hs_data = hashlib.sha256()
        hs_data.update(value.encode("utf-8"))
        return hs_data.hexdigest().upper()

    def get_password(self, client, user_name, method='sha256'):
        timestamp = arrow.now(tz='Asia/Shanghai').timestamp
        value = '{client}{project_id}{method}{timestamp}{secret_key}'.format(
            client=client,
            project_id=self.project_id,
            method=method,
            timestamp=timestamp,
            secret_key=self.secret_key
        )
        sign = self.jm_sha256_single(value)
        return '{client}&{user_name}&{method}&{timestamp}&{sign}'.format(
            client=client,
            user_name=user_name,
            method=method,
            timestamp=timestamp,
            sign=sign
        )

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("Client on_connect called.")
        logging.info("Connected with result code " + str(rc))
        self._client.subscribe("compass/event/monitor/e100.zxy.car9")


    def __enter__(self):
        # 这个地方的client id 是什么都可以  我就是随手用 device tag代替的
        self._client = mqtt.Client(client_id=self.device_tag)
        self._client.username_pw_set(str(self.project_id), self.secret_key)
        self._client.connect(self.host, self.port, 120)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)

    def _on_publish(self, client, userdata, result):
        logging.info("data published")
        pass

    def publish_data(self, data, qos=0):
        # qos = 0 时，消息最多发布一次，可能一次都没收到。
        # qos = 1 时，消息至少发布一次，可能收到多次。
        # qos = 2 时，消息仅发布一次，保证收到且只收到一次。

        topic = '/sys/{project_id}/{device_tag}/sensor/datas'.format(project_id=self.project_id,
                                                                     device_tag=self.device_tag)

        result, _ = self._client.publish(topic, json.dumps(data), qos)
        if result == 0:
            pass
        else:
            raise Exception("This is feature")


def test_tcp():
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
        print(res)
        data = {
            "t": 3,
            "msgid": 2,
            "datatype": 1,
            "datas": {
                "nl_temperature": "27"
            }
        }
        res = t.send_data(payload=data)
        print(res)


def test_mqtt():
    host = "mqtt.nlecloud.com"
    port = 1883
    secret_key = '88d118d83cdf4df79bae18c924c50198'
    user_name = '94635'
    device_tag = '4431Llmqtt'
    porject_id = 13617
    data = {
        "t": 3,
        "msgid": 10159,
        "datatype": 1,
        "datas": {
            "wendu_lwc_1": 69.00,
            "ag_air_temperature": 2
        }
    }
    with MqttRequest(host=host, port=port, porject_id=porject_id, device_tag=device_tag, secret_key=secret_key) as c:
        c.publish_data(data=data, qos=1)


if __name__ == '__main__':
    # test_mqtt()
    # test_tcp()
    pass