import urllib3
import json
import gzip
import base64
from io import BytesIO

http = urllib3.PoolManager()

def lambda_handler(event, context):
    url = "your.discord.webhook.url"
    usename = "custom.username"
    avatar_url = "custom.avatar.url"
    
    # base64 decode하고 gzip 읽어오기
    cw_data = str(event['awslogs']['data'])
    cw_logs = gzip.GzipFile(fileobj=BytesIO(base64.b64decode(cw_data, validate=True))).read()
    log_events = json.loads(cw_logs)
    
    # 보낼 메시지만 뽑아서 payload에 담음. 단 슬랙 메시지에 2000 character 제한이 있기 때문에 전체 메시지를 전부 받아야 한다면 끊어서 보내야 함
    payload=log_events['logEvents'][0]['message']

    # 1990자씩 끊어서 순차적으로 전송
    payloads = [payload[i:i+1990] for i in range(0, len(payload), 1990)]

    msg = {
        "username": usename,
        "content": "",
        "avatar_url": avatar_url
    }

    header = {
        "Content-Type": "application/json"
    }
    # Discord Webhook은 받는 post content-type 제한 있으니 header설정 반드시 해 줘야함
    for payload in payloads:
        msg["content"] = payload
        encoded_msg = json.dumps(msg).encode("utf-8")
        resp = http.request("POST", url, body=encoded_msg, headers=header)
    
    print(
        {
            "message": payload,
            "status_code": resp.status,
            "response": resp.data,
        }
    )
