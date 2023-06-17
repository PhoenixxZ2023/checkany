from crypt import methods
import os
import sys
import typing as t
from datetime import datetime
from flask import Flask, jsonify, request

LISTENING_PORT = int(sys.argv[1])
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

def format_date(date_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    formatted_date = date.strftime("%Y-%m-%d-")
    return formatted_date

def get_user(username: str) -> t.Optional[str]:
    command = 'userscheck %s 1' % username
    result = os.popen(command).readlines()
    final = result[0].strip()
    return final

def cont_online(username: str) -> t.Optional[str]:
    command = 'userscheck %s 2' % username
    result = os.popen(command).readlines()
    final = result[0].strip()
    return final

def limiter_user(username: str) -> t.Optional[str]:
    command = 'userscheck %s 3' % username
    result = os.popen(command).readlines()
    final = result[0].strip()
    return final

def check_data(username: str) -> t.Optional[str]:
    command = 'userscheck %s 4' % username
    result = os.popen(command).readlines()
    final = result[0].strip()
    return final

def check_dias(username: str) -> t.Optional[str]:
    command = 'userscheck %s 5' % username
    result = os.popen(command).readlines()
    final = result[0].strip()
    return final

@app.route('/checkany', methods=['POST', 'GET'])
def check_user():
    if request.method == 'POST':
        try:  
            data = request.form
            username = data.get('username')
            deviceid = data.get('deviceid')
            user = get_user(username)
            if user == "Not exist":  
                return jsonify({
                  "USER_ID": username,
                  "DEVICE": deviceid,
                  "is_active": "false",
                  "Status": "naoencontrado",
                  "uuid": "null"
                })
            else: 
                online = cont_online(user)
                limite = limiter_user(user)
                device = "false" if online > limite else deviceid
                is_active = "false" if online > limite else "true"
                return jsonify({
                  "USER_ID": username,
                  "DEVICE": device,
                  "is_active": is_active,
                  "expiration_date": format_date(check_data(user)),
                  "expiry": f"{check_dias(user)} dias.",
                  "uuid": "null"
                })
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        try:
            return 'Cannot GET /checkany'
        except Exception as e:
            return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(sys.argv[1]) if len(sys.argv) > 1 else LISTENING_PORT
    )
