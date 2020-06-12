from flask import Flask, render_template, request
from config import VK_CLIENT_ID, VK_CLIENT_SECRET
import requests
import json
import db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/auth/vk', methods=['GET'])
def auth_vk():
    vk_code = request.args['code']
    res = requests.get(
        "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://localhost:5000/api/auth/vk".format(
            VK_CLIENT_ID, VK_CLIENT_SECRET, vk_code))
    token = json.loads(res.text)
    if 'error' in token:
        return render_template('index.html')
    res = requests.get("https://api.vk.com/method/users.get?uids={}&access_token={}&v=5.110".format(token['user_id'],
                                                                                                    token[
                                                                                                        'access_token']))
    user_info = json.loads(res.text)['response'][0]
    role = db.get_user(user_info['id']).role
    if role == 'resident':
        pass
    elif role == 'manager':
        pass
    else:
        pass
    return str(user_info['id'])


@app.route('/resident')
def resident():
    return 'resident'


@app.route('/management')
def management():
    return 'Management!'


@app.route('/api/complaints/get')
def complaints_gets():
    return 'Complaints!'


@app.route('/api/complaints/new')
def complaints_new():
    return 'Complaints!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
