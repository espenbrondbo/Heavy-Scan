from __future__ import with_statement
from scapy.all import *
from utils import *


def syn_scan(ip, port, sender=None):
	global TIMEOUT
	ms = getms()
	nttl = random.randint(99, 144)
	
	resp = sr1(IP(dst=ip, src=sender, ttl=nttl)/TCP(dport=port, sport=1337, flags="S"), timeout=TIMEOUT, verbose = 0)
	
	if (resp != None and resp.getlayer(TCP)):
		if resp.getlayer(TCP).flags == 20:
			return False
		elif resp.getlayer(TCP).flags == 18 and resp.getlayer(TCP):
			print str("+(syn scan) "+ str(ip) + ":"+ str(port) + "\tping "+ str(getms() - ms) + "ms")
			try:
				with open("result_of_scan","a+") as f:
					f.write("+(syn scan) "+ str(ip) + ":" + str(port)+ "\n")
			except:
				print "Exception"
			return True
		else:
			print str("+(syn scan) " +str(ip) + ":" +str(port) + "\tflags:" + str(resp.getlayer(TCP).flags))
			return True
	return False
