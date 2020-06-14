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
    res = requests.get(
        "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://116.203.105.221/api/auth/vk".format(
            VK_CLIENT_ID, VK_CLIENT_SECRET, vk_code))
    # res = requests.get(
    #     "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://{}:{}/api/auth/vk".format(
    #         VK_CLIENT_ID, VK_CLIENT_SECRET, vk_code, SERVER_HOST, SERVER_PORT))
    token = json.loads(res.text)
    if 'error' in token:
        return render_template('index.html')
    res = requests.get("https://api.vk.com/method/users.get?uids={}&access_token={}&v=5.110".format(token['user_id'],
                                                                                                    token[
                                                                                                        'access_token']))
    user_info = json.loads(res.text)['response'][0]
    print(user_info)
    role = db.get_user(user_info['id']).role
    if role == 'resident':
        return redirect(url_for('resident', data=user_info['id']))
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
    data = {'name': user.name, 'adverts': adverts, 'vk_id': vk_id}
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
    data = {'name': user.name, 'adverts': adverts, 'vk_id': vk_id}
    return render_template('manager.html', data=data)


@app.route('/api/adverts/add')
def api_add_complaint():
    data = request.args
    if data['option-1'] != '':
        db.add_advert(data['text'], data['option-1'], data['option-2'], data['option-3'])
    else:
        db.add_advert(data['text'])

    return redirect(url_for('manager', data=data['vk_id']))


@app.route('/voiting')
def voiting():
    data = request.args
    advert = db.get_adverts_by_id(data['id'])
    voices_all = int(advert.voice_1) + int(advert.voice_2) + int(advert.voice_3)
    if voices_all != 0:
        percent_1 = int(advert.voice_1) * 100 / voices_all
        percent_2 = int(advert.voice_2) * 100 / voices_all
        percent_3 = int(advert.voice_3) * 100 / voices_all
        percents = [round(percent_1), round(percent_2), round(percent_3)]
    else:
        percents = [0, 0, 0]
    data = {'vk_id': data['data'], 'advert': advert, 'percents': percents}
    return render_template('resident_voiting.html', data=data)


@app.route('/voiting/voice')
def voiting_voice():
    data = request.args
    user = db.get_user(data['data'])
    if data['option'] == '1':
        db.update_advert(id=data['adv_id'], voice_1=user.area)
    elif data['option'] == '2':
        db.update_advert(id=data['adv_id'], voice_2=user.area)
    elif data['option'] == '3':
        db.update_advert(id=data['adv_id'], voice_3=user.area)

    return redirect(url_for('resident', data=data['data']))

@app.route('/voiting/results')
def voiting_results():
    data = request.args
    advert = db.get_adverts_by_id(data['id'])
    voices_all = int(advert.voice_1) + int(advert.voice_2) + int(advert.voice_3)
    if voices_all != 0:
        percent_1 = int(advert.voice_1) * 100 / voices_all
        percent_2 = int(advert.voice_2) * 100 / voices_all
        percent_3 = int(advert.voice_3) * 100 / voices_all
        percents = [round(percent_1), round(percent_2), round(percent_3)]
    else:
        percents = [0, 0, 0]
    data = {'vk_id': data['data'], 'advert': advert, 'percents': percents}
    return render_template('manager_voiting.html', data=data)

@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')
@app.route('/img1')
def img1():
    return render_template('co-hu.html')

@app.route('/img2')
def img2():
    return render_template('co-me.html')

@app.route('/img3')
def img3():
    return render_template('za-hu.html')

@app.route('/img4')
def img4():
    return render_template('za-me.html')

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
