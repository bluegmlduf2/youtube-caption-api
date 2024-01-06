# https://api.ncloud-docs.com/docs/ai-naver-papagonmt-translation
import os
import sys
import urllib.request

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("번역할 문장을 입력하세요")
data = "source=ko&target=en&text=" + encText
url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
request = urllib.request.Request(url)
request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
request.add_header("X-NCP-APIGW-API-KEY", client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if rescode == 200:
    response_body = response.read()
    print(response_body.decode("utf-8"))
else:
    print("Error Code:" + rescode)
