from umqtt.simple import MQTTClient

import machine

import config

import ubinascii

import wifi

import time

import utils

mqttClient = MQTTClient(

    client_id=ubinascii.hexlify(machine.unique_id()),

    server=config.mqtt_server,

    port=config.mqtt_port,

    user=config.mqtt_user,

    password=config.mqtt_password)


# 连接MQTT服务器

def on_mqtt_connect():

    mqttClient.connect()

    on_subscribe('/debug')

    on_subscribe('/subscribe')

    on_publish("/login", bytes('登录时间：%s' %
                               utils.get_datetime(), 'utf-8'))


# 发布消息
def on_publish(topic, payload, retain=False, qos=0):

    mqttClient.publish(topic, payload, retain, qos)


# 消息处理函数

def on_message_come(topic, msg):

    utils.led_blink(0.1)

    print("主题：", topic)

    print("消息：", msg)

    # on_publish("/message", b"收到主题：%s 消息：%s" % (str(topic, 'utf-8'), str(msg, 'utf-8')))
    on_publish("/message", bytes("收到主题：%s 消息：%s" %
               (str(topic, 'utf-8'), str(msg, 'utf-8')), 'uft-8'))

    if topic == b'/debug':
        handle_switch(msg, topic)
    # 添加主题
    if topic == b'/subscribe':

        print("\n订阅：", str(msg, 'utf-8'))

        on_subscribe(str(msg, 'utf-8'))


def handle_switch(msg, topic=b"/debug"):
    if topic == b"/debug":
        # 先分析是状态
        if msg[-2:] == b'on':
            switch_value = 1
        else:
            switch_value = 0

        if switch_value == 1:
            switch_name = msg[:-3]
        else:
            switch_name = msg[:-4]

        switch_name = str(switch_name, 'utf-8')

        # 判断变量是否存在
        try:
            exec('switch.%s' % switch_name)
        except AttributeError:
            switch_name_exists = False
        else:
            switch_name_exists = True

        if switch_name_exists:
            exec('switch.%s = %s' % (switch_name, switch_value))
            print("\n %s：%s" % ('switch.%s' % switch_name, switch_value))
        else:
            print("\n%s不存在" % switch_name)


# 订阅消息
def on_subscribe(Topic='/test'):

    mqttClient.set_callback(on_message_come)

    mqttClient.subscribe(Topic, qos=1)


# 重启服务
def restart_and_reconnect():
    while not wifi.is_connect():

        print("\n 尝试连接wifi，请稍后")

        utils.led_blink(0.1)

        time.sleep(1)

    try:
        print('\n 重新连接mqtt服务器')
        on_mqtt_connect()

    except OSError as e:
        print("尝试连接mqtt服务，发现异常：%s" % e)

        restart()


def restart():
    print("\n 尝试连接mqtt失败，5秒后重启")

    time.sleep(5)

    machine.reset()
