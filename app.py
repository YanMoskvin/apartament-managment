from flask import Flask, render_template, request, redirect, url_for
from config import VK_CLIENT_ID, VK_CLIENT_SECRET, SERVER_PORT, SERVER_HOST
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
    # res = requests.get(
    #     "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://116.203.105.221/api/auth/vk".format(
    #         VK_CLIENT_ID, VK_CLIENT_SECRET, vk_code))
    res = requests.get(
        "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://{}:{}/api/auth/vk".format(
            VK_CLIENT_ID, VK_CLIENT_SECRET, vk_code, SERVER_HOST, SERVER_PORT))
    token = json.loads(res.text)
    if 'error' in token:
        return render_template('index.html')
    res = requests.get("https://api.vk.com/method/users.get?uids={}&access_token={}&v=5.110".format(token['user_id'],
                                                                                                    token[
                                                                                                        'access_token']))
    user_info = json.loads(res.text)['response'][0]
    role = db.get_user(user_info['id']).role
    if role == 'resident':
        return redirect(url_for('manager', data=user_info['id']))
    elif role == 'manager':
        return redirect(url_for('manager', data=user_info['id']))
    else:
        pass
    return 'Вас нет в базе данных. Обратитесь к управляющей компании.'


@app.route('/resident')
def resident():
    data = request.args
    if 'data' not in data:
        return redirect(url_for('.index'))
    vk_id = data['data']
    user = db.get_user(vk_id)
    adverts = db.get_adverts()
    data = {'name': user.name, 'adverts': adverts}
    return render_template('resident.html', data=data)


@app.route('/video')
def management():
    return render_template('video.html')

@app.route('/manager')
def manager():
    data = request.args
    if 'data' not in data:
        return redirect(url_for('.index'))
    vk_id = data['data']
    user = db.get_user(vk_id)
    adverts = db.get_adverts()
    data = {'name': user.name, 'adverts': adverts}
    return render_template('manager.html', data=data)

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
