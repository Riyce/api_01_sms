import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
url = 'https://api.vk.com/method/users.get'
vk_token = os.getenv('VK_TOKEN')
account_sid = os.getenv('TWILLO_ACOOUNT_SID')
auth_token = os.getenv('TWILLO_AUTH_TOKEN')
twillo_number = os.getenv('NUMBER_FROM')
my_number = os.getenv('NUMBER_TO')
client = Client(account_sid, auth_token)
fields = 'online'
version = '5.92'


def get_status(user_id):
    params = {
        'fields': fields,
        'user_ids': user_id,
        'access_token': vk_token,
        'v': version,
    }
    user = requests.post(url, params=params)
    return user.json()['response'][0]['online']


def sms_sender(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=twillo_number,
        to=my_number
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
