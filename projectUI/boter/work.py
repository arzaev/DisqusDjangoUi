import logging
from multiprocessing.dummy import Pool
import random


def go(func, worksheet, threads=1):
	pool = Pool(threads) 
	pool.map(func, worksheet)
	pool.close()
	pool.join()


def get_logger():
	logger = logging.getLogger('server_logger')
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler('data/main.log')
	fh.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)
	formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)
	logger.addHandler(ch)
	logger.addHandler(fh)
	return logger	

def random_key_lowercase(lenght):
	s = "abcdefghijklmnopqrstuvwxyz01234567890"
	passlen = int(lenght)
	key = "".join(random.sample(s, passlen))
	return key

def random_key(lenght):
	s = "abcdefghijklmnopqrstuvwxyz01234567890QWERTYUIOPASDFGHJKLZXCVBNM"
	passlen = int(lenght)
	key = "".join(random.sample(s, passlen))
	return key


