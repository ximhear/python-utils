import requests
import json

# JSON 데이터 준비
json_data = {
    'key1': 'value1',
    'key2': 'value2'
}

# 파일 준비
files = {
    'file': ('filename', open('file_path', 'rb'))
}

# JSON 데이터를 문자열로 변환
json_payload = json.dumps(json_data)

# Multipart/form-data 요청
response = requests.post(
    'http://example.com/api/upload',
    files=files,
    data={'json': json_payload}
)

# 응답 출력
print(response.text)
