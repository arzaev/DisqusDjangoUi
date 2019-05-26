# coding: utf-8

from boter.http import InitBot
from boter.work import go
from main.models import Item
from urllib.parse import quote_plus
import random
import time
import ast
import re


class CheckDisqus(InitBot):
	def __init__(self, item_proxy, type_proxy, user_agent, cookie, login):
		InitBot.__init__(self, item_proxy=item_proxy, type_proxy=type_proxy, user_agent=user_agent)
		self.session.cookies.update(cookie)
		self.login = login

	def likes(self):
		url = 'https://disqus.com/api/3.0/users/details.json?api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': '*/*',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://disqus.com/by/{}/'.format(self.login),
						'X-Requested-With': 'XMLHttpRequest',
						'Connection': 'close',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)
		return int(r.text.split('"numLikesReceived":')[1].split(',')[0])

	def notification(self):
		url = 'https://disqus.com/api/3.0/timelines/getUnreadCount?type=notifications&routingVersion=12&api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': 'application/json, text/javascript, */*; q=0.01',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://disqus.com/by/{}/'.format(self.login),
						'X-Requested-With': 'XMLHttpRequest',
						'Connection': 'close',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)
		return int(r.text.split('"response":')[1].split('}')[0])

	def removed(self, logger):
		TEXT = ''
		cursor = ''
		while True:
			url = 'https://disqus.com/api/3.0/timelines/activities?type=profile&index=comments&target=user%3Ausername%3A{}&cursor={}&limit=10&api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'.format(self.login, cursor)
			headers = {'Host': 'disqus.com',
							'User-Agent': self.user_agent,
							'Accept': 'application/json, text/javascript, */*; q=0.01',
							'Accept-Language': 'en-US,en;q=0.5',
							'Accept-Encoding': 'gzip, deflate',
							'Referer': 'https://disqus.com/by/{}/'.format(self.login),
							'X-Requested-With': 'XMLHttpRequest',
							'Connection': 'close',
							}
			r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)
			TEXT += r.text
			cursor = r.text.split('"next":')[1].split(',')[0]
			logger.info(cursor)
			if cursor == 'null':
				break
			else:
				cursor = cursor.replace('"', '')
		text = TEXT
		listmain = []
		if '"isSpam":true,' in r.text:
			regex = r'"isSpam":true,'
			list = re.findall(regex, text)
			listmain.append('spam')
			listmain.append(str(len(list)))
		if '"isDeleted":true' in r.text:
			regex = r'"isDeleted":true'
			list = re.findall(regex, text)
			listmain.append('rm')
			listmain.append(str(len(list)))
		return listmain


def launch(data):
	try:
		cd = CheckDisqus(item_proxy=data['item_proxy'],
						type_proxy=data['type_proxy'],
						user_agent=data['user_agent'],
						cookie=data['cookie'],
						login=data['login']
						)
		try:
			likes = cd.likes()
		except:
			likes = 0
		try:
			notification = cd.notification()
		except:
			notification = 0

		list_status = cd.removed(data['logger'])
		data['logger'].info('login {} : {}'.format(data['login'], str(list_status)))
		item = Item.objects.get(id=data['id'])
		item.upvotes = likes
		item.notification = notification
		item.status = " ".join(list_status) 
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
		arg['cookie'] = ast.literal_eval(item.cookie)
		arg['user_agent'] = item.user_agent
		accounts.append(arg)
	go(launch, accounts, 50)




