# cloudwatchLogDiscord
cloudwatch log 그룹 구독 필터로 discord 통지 보내기

### 대충 구조
<img width="915" alt="스크린샷 2025-03-17 오전 3 04 49" src="https://github.com/user-attachments/assets/feaeddb5-f182-4c80-9ca7-73c57cf712bb" />
* cloudwatch log 구독 필터로 lambda 트리거링해서 디스코드 메시지 보내기

#### cloudwatch log 통지 json 구조
```json
{
  "awslogs": {
    "data": "base64.encoded.data"
  }
}
```
* KNS 암호화 설정 안했으면 기본적으로 base64 인코딩만 되어있다
* 디코딩하면 gzip으로 압축된 json 데이터가 나오고 구조는 다음과 같은듯함

```json
{
  "messageType": "DATA_MESSAGE",
  "owner": "123456789123",
  "logGroup": "testLogGroup",
  "logStream": "testLogStream",
  "subscriptionFilters": [
    "testFilter"
  ],
  "logEvents": [
    {
      "id": "eventId1",
      "timestamp": 1440442987000,
      "message": "[ERROR] First test message"
    },
  ]
}
```

#### discord webhook api doc
[link](https://discord.com/developers/docs/resources/webhook#execute-webhook)
