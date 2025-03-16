import urllib3
import gzip
import json
import base64
from io import BytesIO

http = urllib3.PoolManager()

def lambda_handler(event, context):
    url = "your.discord.webhook.url"

    # base64 decode하고 gzip 읽어오기
    cw_data = str(event['awslogs']['data'])
    cw_logs = gzip.GzipFile(fileobj=BytesIO(base64.b64decode(cw_data, validate=True))).read()
    log_events = json.loads(cw_logs)

    # 보낼 메시지만 뽑아서 payload에 전송
    payload = log_events['logEvents'][0]['message']

    msg = {
        "username": "AWS php error",
        "content": payload,
    }
    # Discord Webhook은 받는 post content-type 제한 있으니 header설정 반드시 해 줘야함
    header = {
        "Content-Type": "application/json"
    }

    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg, headers=header)
    print(
        {
            "message": payload,
            "status_code": resp.status,
            "response": resp.data,
        }
    )
