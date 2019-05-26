
# coding: utf-8

from requests import Session
import time
from urllib.parse import quote_plus, unquote_plus
import cfscrape


class TempMailOrg:
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
		tokens, user_agent = cfscrape.get_tokens("http://temp-mail.org", proxies=self.proxies, verify=False)
		self.session.cookies.update(tokens)
		self.user_agent = user_agent

	def get_main_page(self):
		url = 'https://temp-mail.org/'
		headers = {'Host': 'temp-mail.org',
						'User-Agent': self.user_agent,
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Connection': 'close',
						'Upgrade-Insecure-Requests': '1',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		###############################################3
#		s = quote_plus(r.text.split('name="s" value="')[1].split('"')[0])
#		jschl_vc = r.text.split('name="jschl_vc" value="')[1].split('"')[0]
#		pass_ = r.text.split('name="pass" value="')[1].split('"')[0]
#		
#		url = 'http://temp-mail.org/cdn-cgi/l/chk_jschl?s=' + s + '&jschl_vc=' + jschl_vc + '&pass=' + pass_ + '&jschl_answer=18.4094314325'
#
#		headers = {'Host': 'temp-mail.org',
#						'User-Agent': self.user_agent,
#						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#						'Accept-Language': 'en-US,en;q=0.5',
#						'Accept-Encoding': 'gzip, deflate',
#						'Referer': 'http://temp-mail.org/',
#						'Connection': 'close',
#						'Upgrade-Insecure-Requests': '1',
#						}
#		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
#
#		url = 'http://temp-mail.org/'
#		headers = {'Host': 'temp-mail.org',
#						'User-Agent': self.user_agent,
#						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#						'Accept-Language': 'en-US,en;q=0.5',
#						'Accept-Encoding': 'gzip, deflate',
#						'Referer': 'http://temp-mail.org/',
#						'Connection': 'close',
#						'Upgrade-Insecure-Requests': '1',
#						}
#		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
#
#		url = 'http://temp-mail.org/'
#		headers = {'Host': 'temp-mail.org',
#						'User-Agent': self.user_agent,
#						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#						'Accept-Language': 'en-US,en;q=0.5',
#						'Accept-Encoding': 'gzip, deflate',
#						'Referer': 'http://temp-mail.org/',
#						'Connection': 'close',
#						'Upgrade-Insecure-Requests': '1',
#						}
#		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		
		###############################################
		my_email = r.text.split('class="emailbox-input opentip" value="')[1].split('"')[0]
		return my_email	

	def check_page(self, mess):
#		url = 'https://temp-mail.org/'
#		headers = {'Host': 'temp-mail.org',
#						'User-Agent': self.user_agent,
#						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#						'Accept-Language': 'en-US,en;q=0.5',
#						'Accept-Encoding': 'gzip, deflate',
#						'Connection': 'close',
#						'Upgrade-Insecure-Requests': '1',
#						}
#		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)

		timer = str(time.time()).split('.')[0]
		url = 'https://temp-mail.org/en/option/check/?_=' + timer
		headers = {'Host': 'temp-mail.org',
						'User-Agent': self.user_agent,
						'Accept': 'text/html, */*; q=0.01',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'https://temp-mail.org/',
						'X-Requested-With': 'XMLHttpRequest',
						'Connection': 'close',
						}

		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		
		if mess in r.text:
			self.url_message = r.text.split(mess)[0].split('href="')[-1]
			return True
		else:
			return False

	def read_mail(self):
		timer = str(time.time()).split('.')[0]
		url = self.url_message + '/?' + timer
		
		headers = {'Host': 'temp-mail.org',
						'User-Agent': self.user_agent,
						'Accept': '*/*',
						'Accept-Language': 'en-US,en;q=0.5',
						'Accept-Encoding': 'gzip, deflate',
						'X-Requested-With': 'XMLHttpRequest',
						'Referer': self.url_message,
						'Connection': 'close',
						}
		r = self.session.get(url, headers=headers, proxies=self.proxies, verify=False, allow_redirects=False)
		return r.text
			

