import re, time, random

ip_home = "127.0.0.1"
ip_test = "31.220.27.193"

TIMEOUT = 0.5

getms = lambda: int(round(time.time() * 1000))

def parse_range(input):
	list = re.split(" *, *", input)
	ret = []
	for token in list:
		if "-" in token:
			list = re.split(" *- *", token)
			for x in range(int(list[0]), int(list[1])+1):
				ret.append(x)
		else:
			ret.append(int(token))
	return ret
	
def wait_for(ms):
	try:
		time.sleep(ms / 1000)
	except:
		pass


