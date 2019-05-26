# coding: utf-8

from boter.http import InitBot
from boter.work import go
from main.models import Item
from boter.tempmailorg import TempMailOrg
from urllib.parse import quote_plus
import random
import time
import ast
import re
import json


class ConfirmEmailDisqus(InitBot):
	def __init__(self, item_proxy, type_proxy, user_agent, cookie, login, password, email):
		InitBot.__init__(self, item_proxy=item_proxy, type_proxy=type_proxy, user_agent=user_agent)
		self.cookie = cookie
		self.session.cookies.update(cookie)
		self.login = login
		self.password = password
		self.email = email

	def start(self):
		url = 'https://disqus.com/home/settings/account/'
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Connection': 'close',
						'Upgrade-Insecure-Requests': '1',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)	

		url = 'https://disqus.com/users/self/account/'
		data = {"username":self.login,
				"email":self.email,
				"password":"",
				"old_password":self.password,
				"email_verified":False}
		data = json.dumps(data)
		
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': 'application/json, text/javascript, */*; q=0.01',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://disqus.com/home/settings/account/',
						'Content-Type': 'application/json',
						'X-CSRFToken': self.cookie['csrftoken'],
						'X-Requested-With': 'XMLHttpRequest',
						'Content-Length': str(len(data)),
						'Connection': 'close',
						}
		r = self.session.put(url, headers=headers, data=data, proxies=self.proxies, verify=False, allow_redirects=False)	
		if r.status_code == 200:
			return True
		return False

	def confirm(self, url):
		referer = url
		headers = {'Host': 'disq.us',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, allow_redirects=False)

		url = r.text.split('"0;URL=')[1].split('"><')[0].replace('&amp;', '&')
		headers = {'Host': 'disqus.com',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': referer,
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify)


def launch(data):
	try:
		tmo = TempMailOrg(proxy=data['item_proxy'],
							type_proxy=data['type_proxy'],
							user_agent=data['user_agent']
							)
		email = tmo.get_main_page()

		cd = ConfirmEmailDisqus(item_proxy=data['item_proxy'],
						type_proxy=data['type_proxy'],
						user_agent=data['user_agent'],
						cookie=data['cookie'],
						login=data['login'],
						password=data['password'],
						email=email
						)
		status = cd.start()
		if status:

			for i in range(20):
				time.sleep(1)
				print(f'wait mail: {i}')
			ans = tmo.check_page('" title="Verify your email now, prevent stuck comments" class="title-subject">Verify your email now, pr')
			if ans:
				t = tmo.read_mail()
				url = 'http://disq.us/url?' + t.split('href="http://disq.us/url?')[1].split('"')[0].replace('&amp;', '&')
				cd.confirm(url)
				item = Item.objects.get(id=data['id'])
				item.status = "confirm email"
				item.email = email
				item.save()
	except Exception as error:
		data['logger'].warning(str(error))


def start(data, logger):
	
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
		arg['password'] = item.password
		arg['cookie'] = ast.literal_eval(item.cookie)
		arg['user_agent'] = item.user_agent
		accounts.append(arg)
	go(launch, accounts, 50)





