# -*- coding: utf-8 -*-
import requests
import os, json
from dotenv import load_dotenv

load_dotenv()


send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기

# ================================================================== 문자 보낼 때 필수 key값
# API key, userid, sender, receiver, msg
# API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용
data_info = json.loads(os.getenv("ALIFO_DATA_INFO"))

sms_data={'key': data_info['apikey'], #api key
        'userid': data_info['aligo_id'], # 알리고 사이트 아이디
        'sender': data_info['sender'], # 발신번호
        # 'receiver': '01000000000', # 수신번호 (,활용하여 1000명까지 추가 가능)
        'receiver': '01033201154', # 수신번호 (본인번호로 테스트 중)
        # 'msg': '%고객명% test', #문자 내용 
        'msg': '알리고 테스트 문자입니다', #문자 내용 
        'msg_type' : 'sms', #메세지 타입 (SMS, LMS)
        # 'title' : 'title', #메세지 제목 (장문에 적용)
        # 'destination' : '01000000000|홍길동', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
}
# print(sms_data)
send_response = requests.post(send_url, data=sms_data)
print (send_response.json())
