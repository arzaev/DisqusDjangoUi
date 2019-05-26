# coding: utf-8

from boter.http import InitBot
from boter.work import go
from main.models import Item
from urllib.parse import quote_plus
import random
import time
import ast
import re


class Like(InitBot):
	def __init__(self, item_proxy, type_proxy, user_agent, cookie, login):
		InitBot.__init__(self, item_proxy=item_proxy, type_proxy=type_proxy, user_agent=user_agent)
		self.session.cookies.update(cookie)
		self.login = login

	def start(self, post):
		url = 'https://disqus.com/api/3.0/posts/vote.json'
		data = 'post={}&vote=1&api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'.format(post)
		headers = {
					'Host': 'disqus.com',
					'User-Agent': self.user_agent,
					'Accept': '*/*',
					'Accept-Language': 'en-US,en;q=0.5',
					'Accept-Encoding': 'gzip, deflate',
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Length': str(len(data)),
					'Connection': 'close'
					}
		r = self.session.post(url, headers=headers, data=data, proxies=self.proxies, verify=False)
		if r.status_code == 200:
			return True
		return False

class Posts:
	def __init__(self, posts, count):
		self.posts = posts
		self.count = count

	def get_post(self):
		if len(self.posts) == 0:
			return None 

		while True:
			post = random.choice(list(self.posts.keys()))
			if self.posts[post] == 3:
				del self.posts[post]
			else:
				self.posts[post] += 1
				return post

def launch(data):
	try:
		l = Like(item_proxy=data['item_proxy'],
						type_proxy=data['type_proxy'],
						user_agent=data['user_agent'],
						cookie=data['cookie'],
						login=data['login']
						)

		while True:
			time.sleep(random.randint(data['sleep_from'], data['sleep_to']))
			post = data['post'].get_post()
			if post == None:
				data['logger'].info('login {} {} '.format(data['login'], 'end'))
				break
			ans = l.start(post)
			if ans:

				item = Item.objects.get(id=int(data['id']))
				base_get = item.base_get
				item.base_get = base_get + 1
				item.save()
				
				data['logger'].info('login {} like {} '.format(data['login'], '200'))
				

		item = Item.objects.get(id=data['id'])
		item.status = "LIKE" 
		item.save()
	except Exception as error:
		data['logger'].warning(str(error))


def start(data, logger):
	
	posts = data['data']['post_id'].split('\n')	
	list_post = []
	post_dict = {}
	for i in posts:
		post_dict[i] = 0
		
	post = Posts(post_dict, int(data['data']['count_like']))

	accounts = []
	for i in data['list']:
		id = int(i)
		item = Item.objects.get(id=id)
		arg = {}
		arg['logger'] = logger
		arg['id'] = id
		arg['item_proxy'] = item.proxy	
		arg['type_proxy'] = item.type_proxy

		arg['sleep_from'] = int(data['data']['sleep_from'])
		arg['sleep_to'] = int(data['data']['sleep_to'])

		arg['login'] = item.login
		arg['cookie'] = ast.literal_eval(item.cookie)
		arg['user_agent'] = item.user_agent
		arg['post'] = post

		item.base_all = int(data['data']['count_like'])
		item.base_get = 0
		item.target = 'LIKE'

		item.save()
		
		accounts.append(arg)


	go(launch, accounts, int(data['data']['threads']))
