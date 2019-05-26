from boter.http import InitBot
from boter.work import go, random_key
from main.models import Item
from urllib.parse import quote_plus
import random
import string
import time
import json
import requests
import ast


class DisqusProfile(InitBot):
	def __init__(self, item_proxy, type_proxy, user_agent, cookie):
		InitBot.__init__(self, item_proxy=item_proxy, type_proxy=type_proxy, user_agent=user_agent)
		self.session.cookies.update(cookie)
		self.cookie = cookie
	

	def start(self, avatar, bio, link):
		url = 'https://disqus.com/home/settings/profile/'
		headers = {'Host': 'disqus.com',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)


		csrftoken = self.cookie['csrftoken']
		name_file = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
		url = 'https://disqus.com/users/self/profile/'
		files = {'avatar_file': ('{}.jpg'.format(name_file), avatar, 'image/jpeg')}
		files2 = {'avatar_source': "computer", 'about': bio, 'url': link, 'is_private': 'true'}
		headers = {'Host': 'disqus.com',
				   'User-Agent': self.user_agent,
				   'Accept': 'application/json, text/javascript, */*; q=0.01',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': 'https://disqus.com/home/settings/profile/',
				   'X-CSRFToken': csrftoken,
				   'X-Requested-With': 'XMLHttpRequest',
				   'Content-Length': str(len(files)),
				   'Connection': 'close',
				   }
		r = self.session.put(url, headers=headers, data=files2, files=files, verify=self.verify, proxies=self.proxies, timeout=self.timeout)
		return r.status_code

	def check_email(self):
		url = 'https://disqus.com/users/self/account/'
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': 'application/json, text/javascript, */*; q=0.01',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://disqus.com/home/settings/account/',
						'X-Requested-With': 'XMLHttpRequest',
						'Connection': 'close',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)
		if '"email_verified":false' in r.text:
			return False
		return True
		
		

def launch(data):
	try:
		mp = DisqusProfile(item_proxy=data['item_proxy'], type_proxy=data['type_proxy'], user_agent=data['user_agent'], cookie=data['cookie'] )
		
		avatar = requests.get('http://' + data['api_host'] + data['avatar']).content
		
		status_code = mp.start(avatar, data['bio'], data['link'])
		data['logger'].info(status_code)
		if status_code == 200:
			item = Item.objects.get(id=data['id'])
			item.profile = True
			data['logger'].info('profile is good: {}: '.format(str(data['id'])))
			if mp.check_email():
				item.save()
			else:
				item.status = 'Email'
				item.save()
		else:
			data['logger'].info('profile is bad: {}: '.format(str(data['id'])))
			
	except Exception as error:
		data['logger'].warning(str(error))


def start(data, logger):

	url = "http://{}/api/images/".format(data['data']['api_host'])
	r = requests.post(url,
		 data={"bot": data['data']['bot'], "network": "disqus", "type": "avatar"},
		 auth=(data['data']['login_api'], data['data']['password_api']))

	avatars = r.json()['avatars']

	url = "http://{}/api/disqusbots/".format(data['data']['api_host'])
	r = requests.post(url,
		 data={"bot": data['data']['bot']},
		 auth=(data['data']['login_api'], data['data']['password_api']))

	bio = r.json()['bio']
	link = r.json()['link']


	accounts = []
	for i in data['list']:
		id = int(i)
		item = Item.objects.get(id=id)
		arg = {}
		arg['logger'] = logger
		arg['id'] = id
		arg['item_proxy'] = item.proxy	
		arg['type_proxy'] = item.type_proxy

		arg['login'] = item.login
		arg['cookie'] = ast.literal_eval(item.cookie)
		arg['bio'] = str(random.choice(bio)).strip()
		arg['link'] = str(random.choice(link)).strip()
		arg['user_agent'] = item.user_agent

		arg['api_host'] = data['data']['api_host']
		arg['bot'] = data['data']['bot']
		arg['login_api'] = data['data']['login_api']
		arg['password_api'] = data['data']['password_api']
		arg['avatar'] = random.choice(avatars)
		accounts.append(arg)
	go(launch, accounts, 10)


