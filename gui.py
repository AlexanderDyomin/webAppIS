from flask import Flask, render_template
import requests

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
	storehouse_from = '<select name = \'storehouse_in\'>' + ''.join(storehouse)
	storehouse_to = '<select name = \'storehouse_out\'>' + ''.join(storehouse)
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
	return render_template('ResManagerTextFrameCreateRequest.html', storehouse_from = storehouse_from
		, storehouse_to = storehouse_to, customer = customer_str, provider = provider)
		
@app.route('/create_new_request', methods = ['POST'])
def send_new_request():
	r = requests.post('')

if __name__ == '__main__':
	app.run(debug = True)