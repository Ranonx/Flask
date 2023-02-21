from flask import Flask
from flask import request
from hashlib import md5
import requests

app = Flask(__name__)

def generate_md5(fp):
    m = md5()
    m.update(fp)
    return m.hexdigest()

def send(phone,inputName,BookDate,BookTime):
    url = 'https://api.sendcloud.net/smsapi/send'
    SMS_USER = 'EDDI_USER'
    SMS_KEY = 'xDdZ9fihSaXQIV6HzDs533eW2RiF4tQw'

    param = {
        'smsUser': SMS_USER,
        'templateId' :902407,
        'msgType': 0,
        'phone' : phone,
        'vars' : f'{{"%name%": {inputName}, "%date%": {BookDate}, "%time%": {BookTime}}}'
    }

    param_keys = list(param.keys())
    param_keys.sort()

    param_str = ""
    for key in param_keys:
        param_str += key + '=' + str(param[key]) + '&'
    param_str = param_str[:-1]

    sign_str = SMS_KEY + '&' + param_str + '&' + SMS_KEY
    sign = generate_md5(sign_str.encode())

    param['signature'] = sign

    res = requests.post(url,data=param)
    return str(res.text)

@app.route('/relay', methods=['POST'])
def handle_json():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        try:
            data = request.json
            phone = data['phone']
            inputName = data['name']
            BookDate = data['date']
            BookTime = data['time']
            return send(phone, inputName, BookDate, BookTime)
        except (KeyError, TypeError):
            return "Invalid JSON data.", 400
    else:
        return "Unsupported content type.", 415

if __name__ == '__main__':
    app.run(debug=True)
