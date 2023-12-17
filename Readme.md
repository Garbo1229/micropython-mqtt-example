# micropython-mqtt-example

## 环境准备
参考：[MicroPthon环境搭建笔记（ESP8266例子和坑）](https://garbo.me/micropthon/MicroPython%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E7%AC%94%E8%AE%B0/)

## 实现功能
通过`ESP32/ESP8266`连接`hc501`传感器,将结果传至`mqtt`服务器达到监控作用

## 上传代码
1. 将`wifi`和`mqtt`服务器配置填写至`config.py`文件中，通用io口默认13是led、15是人体红外，`switch.py`确定需要开启的选项
2. 通过`ampy -p 端口号 put 文件名`上传代码
3. 全部文件上传后点击复位按键启动即可
4. 使用`picocom`命令或软件`uPyCraft`查看运行情况

## mqtt主题说明
- 订阅
    - `esp32/room` : 人体红外传感器感知移动
    - `esp32/login` : 连接mqtt服务器时间
    - `esp32/message` : 接收主题和消息数据
- 发布
    - `esp32/subscribe` : 回复消息动态添加订阅主题
    - `esp32/debug` : 回复消息用于调试，开启固定格式：参数 `on`; 关闭固定格式：参数 `off`; 例子：`led_switch on`;
        - `debug_mode` : 开启人体红外
        - `led_switch` : 关闭人体红外
        - `sync_time_show` : 同步nfp倒数时间
        - `hc_switch` : 开启调试模式（仅打印人体红外未检出移动）

## LED状态
- 长期闪烁 : wifi未连接成功
- 闪烁1次 : 接收一次消息
- 闪烁10次 : 人体红外检测到移动(检测间隔一分钟)

## TODO
- 异步处理
