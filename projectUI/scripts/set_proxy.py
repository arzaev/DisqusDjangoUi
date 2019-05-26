import random
from main.models import Item

def set_proxy(data, logger):
	items = data['list']
	proxies = str(data['data']['proxy']).split('\n')
	type_proxy = str(data['data']['type_proxy'])

	random.shuffle(proxies)
	count_proxy = 0

	for i in items:
		try:
			acc = Item.objects.get(id=int(i))
			logger.info('set proxy {} for item: {}'.format(acc.login, proxies[count_proxy]))
			acc.proxy = proxies[count_proxy]
			acc.type_proxy = type_proxy
			acc.save()
			count_proxy += 1
		except SyntaxError:
			pass
		except IndexError:
			count_proxy = 0
			acc = Item.objects.get(id=int(i))
			logger.info('set proxy {} for item: {}'.format(acc.login, proxies[count_proxy]))
			acc.type_proxy = type_proxy
			acc.proxy = proxies[count_proxy]
			acc.save()
			count_proxy += 1


