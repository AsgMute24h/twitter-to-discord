Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import requests
... import json
... 
... # 트위터 API 인증 정보
... BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIb7yQEAAAAAn2GD2%2FR5qlg71eHvwByq2DDZY6k%3Dr6r5ymiZlghmgXc41lCeJ7Wul24EM4R5CdrNqmaOpIJUgQi0ZZ"
... DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1333054302498979894/kGpf87S-lZvIPFLXxN_bo4K6h-P-2HVLN1mzueGuYNf040FYZWObdeZSNERE3MMOyJXO"
... 
... # 트위터 API 헤더
... headers = {
...     "Authorization": f"Bearer {BEARER_TOKEN}",
...     "Content-Type": "application/json",
... }
... 
... # 1. 스트림 규칙 추가
... def add_stream_rule(username):
...     url = "https://api.twitter.com/2/tweets/search/stream/rules"
...     data = {"add": [{"value": f"from:{Run_FFXIV}"}]}  # 특정 계정 필터링
...     response = requests.post(url, headers=headers, json=data)
...     if response.status_code == 201 or response.status_code == 200:
...         print("스트림 규칙 추가 완료!")
...     else:
...         print(f"스트림 규칙 추가 실패: {response.status_code} - {response.text}")
... 
... # 2. 스트림 시작
... def start_stream():
...     url = "https://api.twitter.com/2/tweets/search/stream"
...     response = requests.get(url, headers=headers, stream=True)
...     if response.status_code == 200:
...         print("스트림 연결 성공. 실시간 트윗 감지 중...")
...         for line in response.iter_lines():
...             if line:
...                 tweet = json.loads(line)
...                 send_to_discord(tweet)
...     else:
        print(f"스트림 연결 실패: {response.status_code} - {response.text}")

# 3. 디스코드로 트윗 전송
def send_to_discord(tweet):
    tweet_id = tweet["data"]["id"]
    text = tweet["data"]["text"]
    content = f"새 트윗이 올라왔어요: {text}\n링크: https://twitter.com/{USERNAME}/status/{tweet_id}"
    payload = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("디스코드 전송 성공!")
    else:
        print(f"디스코드 전송 실패: {response.status_code} - {response.text}")

# 실행
if __name__ == "__main__":
    USERNAME = "Run_FFXIV"  # 모니터링할 계정
    add_stream_rule(USERNAME)  # 필터 규칙 추가
    start_stream()  # 실시간 스트림 시작
