# coding: utf-8

from boter.http import InitBot
from boter.work import go
from main.models import Item
from urllib.parse import quote_plus
import random
import string
import time
import ast
import requests
from PIL import Image, ImageDraw
import io


class SpamPhoto(InitBot):
	def __init__(self, item_proxy, type_proxy, user_agent, cookie):
		InitBot.__init__(self, item_proxy=item_proxy, type_proxy=type_proxy, user_agent=user_agent)
		self.session.cookies.update(cookie)
		self.timeout = 30

	def start(self, url_main, photo):
		url_main = str(url_main).strip().replace('%0D', '')
		headers = {'Host': 'disqus.com',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url_main, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)

		name = str(url_main).split('/')[-2]
		forum = str(url_main).split('discussion/')[1].split('/')[0]

		url = 'https://disqus.com/api/3.0/threads/details?thread=slug%3A{}&forum={}&attach=topics&related=forum' \
			  '&api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'.format(name, forum)
		headers = {'Host': 'disqus.com',
				   'User-Agent': self.user_agent,
				   'Accept': 'application/json, text/javascript, */*; q=0.01',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': url_main,
				   'X-Requested-With': 'XMLHttpRequest',
				   'Connection': 'close',
				   }
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)
		t_e = quote_plus(r.text.split('"clean_title":"')[1].split('"')[0])
		try:
			t_u = r.text.split('"signedLink":"http://disq.us/?url=')[1].split('&k')[0]
		except:
			t_u = r.text.split('"signedLink":"https://disq.us/?url=')[1].split('&k')[0]

		url2 = 'https://disqus.com/embed/comments/?base=default&f={}' \
			   '&t_u={}' \
			   '&t_e={}' \
			   '&t_d={}' \
			   '&t_t={}' \
			   '&s_o=popular'.format(forum, t_u, t_e, t_e, t_e)
		referer = url2
		headers = {'Host': 'disqus.com',
				   'User-Agent': self.user_agent,
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Language': 'en-US,en;q=0.5',
				   'Accept-Encoding': 'gzip, deflate',
				   'Referer': url_main,
				   'Connection': 'close',
				   'Upgrade-Insecure-Requests': '1',
				   }
		r = self.session.get(url2, headers=headers, proxies=self.proxies, verify=self.verify, timeout=self.timeout)
		thread = r.text.split('"thread":"')[1].split('"')[0]

		name_file = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
		files = {'upload': ('{}.jpg'.format(name_file), photo, 'image/jpeg')}
		files2 = {'permanent': '1'}
		url = 'https://uploads.services.disqus.com/api/3.0/media/create.json?api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
		headers = {'Host': 'uploads.services.disqus.com',
						'User-Agent': self.user_agent,
						'Accept': '*/*',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': referer,
						'Content-Length': str(len(files)),
						'Origin': 'https://disqus.com',
						'Connection': 'close',
						}
		r = self.session.post(url, headers=headers, data=files2, files=files, verify=self.verify, proxies=self.proxies, timeout=self.timeout)

		server_img = r.text.split('{"url": "')[1].split('"')[0]
		server_img = quote_plus(server_img)

		data = 'url=' + server_img + '&api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
		url = 'https://disqus.com/api/3.0/media/details.json'
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': '*/*',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': referer,
						'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
						'X-Requested-With': 'XMLHttpRequest',
						'Content-Length': str(len(data)),
						'Connection': 'close',
						}
		r = self.session.post(url, headers=headers, data=data, verify=self.verify, proxies=self.proxies, timeout=self.timeout)

		data = 'thread=' + thread + '&message=' + server_img + '&api_key=E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F'
		url = 'https://disqus.com/api/3.0/posts/create.json'
		headers = {'Host': 'disqus.com',
						'User-Agent': self.user_agent,
						'Accept': '*/*',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': referer,
						'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
						'X-Requested-With': 'XMLHttpRequest',
						'Content-Length': str(len(data)),
						'Connection': 'close',
						}
		r = self.session.post(url, headers=headers, data=data, verify=self.verify, proxies=self.proxies, timeout=self.timeout)
		if r.status_code == 200:
			try:
				self.id_post = r.text.split('"post":"')[1].split('"')[0]
				return True
			except IndexError:
				self.id_post = r.text.split('"id":"')[1].split('"')[0]
				return True
		else:
			return False




def launch(data):
		st = SpamPhoto(item_proxy=data['item_proxy'],
						type_proxy=data['type_proxy'],
						user_agent=data['user_agent'],
						cookie=data['cookie']
						)
		list_code_400 = []
		data['logger'].info('size of base for {} is {}'.format(data['login'], str(len(data['base']))))
		for url in data['base']:
			try:
				time.sleep(random.randint(data['sleep_from'], data['sleep_to']))
				data['logger'].info('login {} trying to comment is {}'.format(data['login'], url))
				photo = random.choice(data['photos'])

	
				image_data = requests.get('http://' + data['api_host'] + photo).content
				image = Image.open(io.BytesIO(image_data))
				d = ImageDraw.Draw(image)
								
				x = random.randint(1, 10)
				y = random.randint(1, 10)

				text = '.'

				r = random.randint(1, 255)
				g = random.randint(1, 255)
				b = random.randint(1, 255)

				d.text((x,y), text, fill=(r,g,b))

				byteIO = io.BytesIO()
				image.save(byteIO, format='JPEG')
				photo = byteIO.getvalue()
				
				
				if st.start(url, photo):
					data['logger'].info('comment 200 {} : {}'.format(data['login'], url))
					item = Item.objects.get(id=int(data['id']))
					base_get = item.base_get
					item.base_get = base_get + 1
#					storage = str(item.storage_base) + '\n' + url
#					item.storage_base = storage
					id_post = st.id_post
					storage = str(item.storage_post) + '\n' + id_post
					item.storage_post = storage
					item.save()
				else:
					data['logger'].info('comment 400 {} : {}'.format(data['login'], url))
					list_code_400.append(400)
					if len(list_code_400) == 10:
						item = Item.objects.get(id=int(data['id']))
						item.status = 'STOP'
						item.save()
						break
			except Exception as error:
				data['logger'].warning(str(error))


def start(data, logger):
	url = "http://{}/api/images/".format(data['data']['api_host'])
	r = requests.post(url,
		 data={"bot": data['data']['bot'], "network": "disqus", "type": "photo"},
		 auth=(data['data']['login_api'], data['data']['password_api']))

	photos = r.json()['photos']
	
	base = str(data['data']['base']).split('\n')
	count_base = 0
	
	action_count = int(len(base) / len(data['list']))

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

		arg['sleep_from'] = int(data['data']['sleep_from'])
		arg['sleep_to'] = int(data['data']['sleep_to'])

		arg['api_host'] = data['data']['api_host']
		arg['bot'] = data['data']['bot']
		arg['login_api'] = data['data']['login_api']
		arg['password_api'] = data['data']['password_api']

		arg['photos'] = photos

		tmp_base = []
		for bar in range(action_count):
			tmp_base.append(base[count_base])
			count_base += 1
			
		arg['base'] = tmp_base
		item.base_all = len(tmp_base)
		item.base_get = 0
		item.target = data['data']['target']
		item.storage_base = "\n".join(tmp_base)
		item.save()

		accounts.append(arg)
	go(launch, accounts, int(data['data']['threads']))




