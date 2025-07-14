import requests
import base64

# API 정보
url = "https://www.ailabapi.com/api/image/editing/ai-image-extender"
api_key = "H8zZOZF4ojlt2Rya3siWbB7NUTO6oY45vcDD1vqb5XB79QmJEUMaCeumrfpCJrjk"

# 이미지 경로
image_path = r"C:\Users\jyes_semin\Desktop\Data\ex.png"

# 파라미터 설정
payload = {
    'custom_prompt':"Please make the image clearer while enlarging it.",
    'steps': '30',
    'strength': '0.8',
    'scale': '7',
    'seed': '0',
    'top': '0.5',
    'bottom': '0.5',
    'left': '0.5',
    'right': '0.5',
    'max_height': '1920',
    'max_width': '1920'
}

# 헤더 설정
headers = {
    'ailabapi-api-key': api_key
}

# 파일 열기 및 POST 요청
with open(image_path, 'rb') as img_file:
    files = {
        'image': ('test.png', img_file, 'application/octet-stream')
    }

    response = requests.post(url, headers=headers, data=payload, files=files)

# 결과 처리
print("응답 코드:", response.status_code)

if response.status_code == 200:
    try:
        base64_str = response.json()["data"]["binary_data_base64"][0]
        image_data = base64.b64decode(base64_str)

        with open("output.jpg", "wb") as f:
            f.write(image_data)

        print("✅ 이미지 저장 완료: output.jpg")
    except Exception as e:
        print("❌ 응답 파싱 오류:", e)
else:
    print("❌ 이미지 생성 실패")
    print(response.text)
