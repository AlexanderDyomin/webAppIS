from flask import Flask, render_template, request, flash, url_for, redirect
import requests
import json
from datetime import datetime

app = Flask(__name__, template_folder = '.')

@app.route('/create_new_request', methods = ['GET'])
def create_new_request():
    s = requests.get('http://kokoserver.me:8090/storehouse/')
    s_json = s.json()
    storehouse = []
    for i in s_json:
        storehouse.append('<option value = \'')
        storehouse.append(str(i['id']))
        storehouse.append('\'>')
        storehouse.append(str(i['name']))
        storehouse.append('</option>')
    storehouse.append('</select>')
    storehouse_from = '<select name = \'storehouse_from\'>' + ''.join(storehouse)
    storehouse_to = '<select name = \'storehouse_to\'>' + ''.join(storehouse)
    c = requests.get('http://kokoserver.me:8090/customer/')
    c_json = c.json()
    customer = []
    for i in c_json:
        customer.append('<option value = \'')
        customer.append(str(i['id']))
        customer.append('\'>')
        customer.append(str(i['company']['name']))
        customer.append('</option>')
    customer.append('</select>')
    customer_str = '<select name = \'customer\'>' + ''.join(customer)
    provider = '<select name = \'provider\'>' + ''.join(customer)
    # return "PIZDECCO TOTALE"
    return render_template('ResManagerTextFrameCreateRequest.html', storehouse_from = storehouse_from, storehouse_to = storehouse_to, customer = customer_str, provider = provider)
        
@app.route('/create_new_request', methods = ['POST'])
def send_new_request():
    # r = request.form['create_request']
    i = requests.get('http://kokoserver.me:8090/product/')
    i_json = i.json()
    r_dict = {}
    r_dict['id_customer'] = request.form['customer']
    # r_dict['id_storehouse_from'] = request.form['storehouse_from']
    r_dict['id_storehouse_to'] = request.form['storehouse_to']
    r_dict['items'] = []
    t = False
    
    for i, j in zip(request.form.getlist('item_name'), request.form.getlist('item_count')):
        if i == '' or j == '':
            continue
        for k in i_json:
            if k['name'] == i:
                r_dict['items'].append({'id_product' : str(k['id']), 'count' : str(j)})
                t = True
                break
    if(t != True):
        # flash('Вы можете добавиь только товары, которые есть в БД!')
        return redirect(url_for('create_new_request'))
    r_dict['operationType'] = request.form['type']
    r_dict['dateBegin'] = datetime.now().strftime('%Y-%m-%d')
    r_dict['id_author'] = '1'
    r_json = json.dumps(r_dict)
    r = requests.post('http://kokoserver.me:8090/request/', json = r_json)
    return str(r.status_code)
    # return r_json

if __name__ == '__main__':
    app.run(debug = True)