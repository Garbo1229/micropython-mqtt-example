import time

import utils

import wifi

import config

import mqtt

import switch

from machine import Pin


def main():

    print("\n系统开启")

    hc = Pin(config.gpio_hc, Pin.IN)  # 人体红外

    wifi.connect_wifi()  # 连接wifi

    # 同步时间

    utils.sync_ntp()

    try:

        mqtt.on_mqtt_connect()  # 连接mqtt服务器

        sync_time = 0

        while True:
            try:
                mqtt.mqttClient.check_msg()  # 检查未处理消息 注：wait_msg() 阻塞式

                mqtt.mqttClient.ping()  # 保持mqtt连接

                sync_time += 1

                time.sleep(1)
                # 定期同步ntp
                if sync_time == 28800:

                    utils.sync_ntp()

                    sync_time = 0

                # 显示倒数时间
                if switch.sync_time_show == 1:

                    print("\n倒数", 28800-sync_time, "秒同步时间")

                # 人体红外
                if switch.hc_switch == 1:

                    if (hc.value() == 1):

                        utils.handle_people(0.5)

                    elif switch.debug_mode != 0:

                        print("\n未检测到移动")

            except OSError as e:

                print("发现异常：%s" % e)

                mqtt.restart_and_reconnect()

    except OSError as e:
        print("尝试连接mqtt服务，发现异常：%s" % e)
        mqtt.restart_and_reconnect()


if __name__ == "__main__":

    main()
