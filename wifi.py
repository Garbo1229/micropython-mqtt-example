
from network import WLAN

from network import STA_IF

from time import sleep_ms

from gc import mem_free

import utils

import config


def is_connect():
    return WLAN(STA_IF).isconnected()


def connect_wifi():

    print("\n可用内存: %s Byte" % str(mem_free()))

    wlan = WLAN(STA_IF)

    wlan.active(True)

    if not wlan.isconnected():

        print("\n当前设备未联网，正在连接 ....")

        wlan.connect(config.wifi_ssid, config.wifi_passwd)

        while not wlan.isconnected():
            print("\n 尝试连接wifi，请稍后")

            sleep_ms(500)

            utils.led_blink(0.1)

            if wlan.isconnected():

                break

    if wlan.isconnected():

        IP_info = wlan.ifconfig()

        print("Wifi信息:")

        print("IP 地址 : " + IP_info[0])

        print("子网掩码 : " + IP_info[1])

        print("网关 : " + IP_info[2])

        print("DNS : " + IP_info[3])

    utils.led_blink(1)
