# 公众号：Python实用宝典
import requests


# 发送
def send_weixin(content):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx"  # 这里就是群机器人的Webhook地址
    headers = {"Content-Type": "application/json"}  # http数据头，类型为json
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content,  # 让群机器人发送的消息内容。
            "mentioned_list": [],
        }
    }
    r = requests.post(url, headers=headers, json=data)  # 利用requests库发送post请求


# 处理逻辑
def logical_processing(data_list, pro_name, index, count):
    context = add_color(data_list)
    if context == 0:
        return context
    tmp = "AWVS扫描结果(已扫描：" + str(index) + "/" + str(count) + "):\n域名/IP:" + pro_name + "\n漏洞数量:\n"
    context += tmp
    for k, v in data_list.items():
        if v != 0:
            tmp = "    "+str(k) +":"+ str(v)+"\n"
            context = context + tmp

    context = context + f"</font>"
    send_weixin(context)


def add_color(vul_info):
    if vul_info["high"] > 0:
        return f"<font color='red'>"
    elif vul_info["medium"] > 0:
        return f"<font color='yellow'>"
    elif vul_info["low"] > 0:
        return f"<font color='blue'>"
    elif vul_info["info"] > 0:
        return f"<font color='gray'>"
    else:
        return 0
