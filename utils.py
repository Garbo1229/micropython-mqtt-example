from machine import Pin, RTC

import ntptime

import mqtt

import time

import switch

import config

move_time = 0


# 通用io的led灯闪烁
def gpio_led_blink(long=0.1, gpid=config.gpio_led):
    if switch.led_switch:
        gpio_led = Pin(gpid, Pin.OUT)

        gpio_led.on()

        time.sleep(long)

        gpio_led.off()

        time.sleep(long)


# led灯闪烁
def led_blink(long=0.1):
    if switch.led_switch:
        led = Pin(2, Pin.OUT)

        led.value(1)  # Set led turn on

        time.sleep(long)

        led.value(0)  # Set led turn off

        time.sleep(long)


# ntp同步
def sync_ntp():

    ntptime.NTP_DELTA = 3155644800  # UTC+8 3155644800 东八区

    ntptime.host = 'ntp1.aliyun.com'

    while True:

        try:

            print("\n尝试推送")  # 可能存在失败

            time.sleep(0.5)

            ntptime.settime()

        except Exception as e:

            print("\n推送失败：%s" % e)

        else:

            print('\n推送成功')

            break

    print("\nntp同步完成")

    return True


# 获取原始日期
def datetime():

    rtc = RTC()

    return rtc.datetime()


# 获取日期 样式:Y-m-d H:i:s
def get_datetime():

    date = datetime()

    return str(date[0]) + '-' + str(date[1]) + '-' + str(date[2]) + ' ' + str(date[4]) + ':' + str(date[5]) + ':' + str(date[6])


# 获取星期
def get_week():

    date = datetime()

    return str((int(date[3]) + 1) % 8)


# 人体红外方法
def handle_people(second=0.5):

    global move_time

    if time.time() > (move_time + 60):  # 一分钟间隔检测

        date = get_datetime()

        mqtt.on_publish(
            "/room", b'{"code":"1","msg":"moving","data":"","datetime":"%s"}' % (date))

        print('【' + date + '】' + '[星期' + get_week() + ']', '有人移动(间隔一分钟检测)')

        move_time = time.time()

        for i in range(10):

            led_blink((second / 2))
