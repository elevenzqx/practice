# coding: utf-8
import _thread as thread
import os
import time
import base64

import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed
import os


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    print(data)
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content,end='')
        if status == 2:
            print("#### 关闭会话")
            ws.close()


def gen_params(appid, query, domain):
    """
    通过appid和用户的提问来生成请参数
    """

    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",           
            # "patch_id": []    #接入微调模型，对应服务发布后的resourceid          
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": query}]
            }, 
            "functions": {
                "text": [
                    {
                        "name": "卡顿",
                        "description": "卡顿插件可以提供问题分析总结。你可以提供指定的用户号码、指定的日期信息、出现的问题\n你只需要将文本信息整理后返回，不需要做其它的处理",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "description": "日期"
                                },
                                "uid": {
                                    "type": "string",
                                    "description": "用户号码，用数字组成"
                                },
                                "message": {
                                    "type": "string",
                                    "description": "用户出现的内容"
                                }
                            },
                            "required": [
                                "time", "uid"
                            ]
                        }
                    },
                    # {
                    #     "name": "天气查询",
                    #     "description": "天气插件可以提供天气相关信息。你可以提供指定的地点信息、指定的时间点或者时间段信息，来检索诗词库，精准检索到天气信息。",
                    #     "parameters": {
                    #         "type": "object",
                    #         "properties": {
                    #             "location": {
                    #                 "type": "string",
                    #                 "description": "地点，比如北京。"
                    #             },
                    #             "date": {
                    #                 "type": "string",
                    #                 "description": "日期。"
                    #             }
                    #         },
                    #         "required": [
                    #             "location"
                    #         ]
                    #     }
                    # },
                    # {
                    #     "name": "税率查询",
                    #     "description": "税率查询可以查询某个地方的个人所得税率情况。你可以提供指定的地点信息、指定的时间点，精准检索到所得税率。",
                    #     "parameters": {
                    #         "type": "object",
                    #         "properties": {
                    #             "location": {
                    #                 "type": "string",
                    #                 "description": "地点，比如北京。"
                    #             },
                    #             "date": {
                    #                 "type": "string",
                    #                 "description": "日期。"
                    #             }
                    #         },
                    #         "required": [
                    #             "location"
                    #         ]
                    #     }
                    # }
                ]
            }
        }
    }
    return data


def main(appid, api_secret, api_key, gpt_url, domain, query):
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.query = query
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    main(
        appid="",
        api_secret="",
        api_key="",
        #appid、api_secret、api_key三个服务认证信息请前往开放平台控制台查看（https://console.xfyun.cn/services/bm35）
        gpt_url="wss://spark-api.xf-yun.com/v3.5/chat",
        # Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
        # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
        # Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
        domain="generalv3.5",
        # domain = "generalv3"    # v3.0版本
        # domain = "generalv2"    # v2.0版本
        # domain = "general"    # v2.0版本
        query="183365575号码 今天3点10分的卡顿记录"
    )
