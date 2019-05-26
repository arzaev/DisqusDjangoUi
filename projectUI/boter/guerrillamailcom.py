
# coding: utf-8

from requests import Session
import time
from urllib.parse import quote_plus, unquote_plus


class Guerrillamail:
	def __init__(self, **kwargs):
		self.proxy = kwargs['proxy']
		self.type_proxy = kwargs['type_proxy']
		if self.type_proxy == 'socks5':
			self.proxies = {
				'http': 'socks5://{}'.format(kwargs['proxy']),
				'https': 'socks5://{}'.format(kwargs['proxy'])
			}
		else:
			if '@' in kwargs['proxy']:
				self.proxies = {'http': 'http://{}'.format(kwargs['proxy']),
								'https': 'https://{}'.format(kwargs['proxy'])}
			else:
				self.proxies = {'http': kwargs['proxy'], 'https': kwargs['proxy']}
		self.user_agent = kwargs['user_agent']
		self.session = Session()

	def get_main_page(self):
		url = 'https://www.guerrillamail.com/inbox'
		headers = {'Host': 'www.guerrillamail.com',
						'User-Agent': self.user_agent,
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Connection': 'close',
						'Upgrade-Insecure-Requests': '1',
						}

		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		email = r.text.split('"email":"')[1].split('"')[0]
		self.email = email
		return email	

	def check_page(self, mess):
		url = 'https://www.guerrillamail.com/inbox'
		headers = {'Host': 'www.guerrillamail.com',
						'User-Agent': self.user_agent,
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Connection': 'close',
						'Upgrade-Insecure-Requests': '1',
						}

		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)	
		if mess in r.text:
			self.unread = r.text.split('email_unread" id="')[1].split('"')[0]
			self.api_token = r.text.split("api_token : '")[1].split("'")[0]
			return True
		else:
			return False

	def read_mail(self):
		timer = str(time.time()).split('.')[0]
		url = 'https://www.guerrillamail.com/ajax.php?f=fetch_email&email_id={}&site=guerrillamail.com&in={}&_={}'.format(self.unread,
																															 self.email.split('@')[0],
																															timer) 
		headers = {'Host': 'www.guerrillamail.com',
						'User-Agent': self.user_agent,
						'Accept': 'application/json, text/javascript, */*; q=0.01',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://www.guerrillamail.com/inbox',
						'Authorization': 'ApiToken {}'.format(self.api_token),
						'X-Requested-With': 'XMLHttpRequest',
						'Connection': 'close',
						}

		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		return r.text
			
