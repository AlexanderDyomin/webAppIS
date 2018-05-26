from flask import Flask, render_template, request, flash, url_for, redirect
import requests
from datetime import datetime
import json

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
    r_dict['dateBegin'] = datetime.now().strftime('%d.%m.%Y')
    r_dict['id_author'] = '1'
    r_json = json.dumps(r_dict)
    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
    r = requests.post('http://kokoserver.me:8090/request/', data = r_json, headers = headers)
    if r.status_code == 200:
        return render_template('ResManagerTextFrameCreateTransportation.html', first_time = True, ok = True, request_id = str(r.text))
    return render_template('ResManagerTextFrameCreateTransportation.html', first_time = True, ok = False)

@app.route('/create_transportation', methods = ['GET'])
def create_new_transportation():
    # request_id = request.form['request_id']
    request_id = str(request.args['request_id'])
    t = requests.get('http://kokoserver.me:8090//transportCompany/')
    t_json = t.json()
    transport_company = []
    for tp in t_json:
        transport_company.append('<option value = \'')
        transport_company.append(str(tp['company']['id']))
        transport_company.append('\'>')
        transport_company.append(tp['company']['name'])
        transport_company.append('</option>')
    transport_company.append('</select>')
    transport_company_str = '<select name = \'transport_company\'>' + ''.join(transport_company)
    return render_template('ResManagerTextFrameCreateTransportation.html', first_time = False, request_id = str(request_id)
        , transport_company = transport_company_str)
    
@app.route('/create_transportation', methods = ['POST'])
def send_new_transportation():
    rq = requests.get('http://kokoserver.me:8090/transportation/')
    rq_json = rq.json()
    for r in rq_json:
        if int(request.form['request_id']) == int(r['request']['id']):
            return "Такая транспортировка уже существует!"
    t_dict = {}
    t_dict['grossWeight'] = request.form['gross_weight']
    t_dict['packingList'] = {}
    # t_dict['packingList'].append({'info': str(request.form['packing_list'])})
    t_dict['packingList']['info'] = str(request.form['packing_list'])
    t_dict['waybill'] = {}
    # t_dict['waybill'].append({'transportCompanyId': str(request.form['transport_company']), 'info': str(request.form['waybill'])})
    t_dict['waybill']['transportCompanyId'] = str(request.form['transport_company'])
    t_dict['waybill']['info'] = str(request.form['waybill'])
    t_dict['id_request'] = request.form['request_id']
    t_json = json.dumps(t_dict)
    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
    r = requests.post('http://kokoserver.me:8090/transportation/', data = t_json, headers = headers)
    return str(r.status_code);

if __name__ == '__main__':
    app.run(debug = True)