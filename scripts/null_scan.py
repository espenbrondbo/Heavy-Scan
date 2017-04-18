from scapy.all import *
from utils import *


def null_scan(ip, port):
	global TIMEOUT
	ms = getms()
	
	resp = sr1(IP(dst=ip)/TCP(dport=port, sport=1337, flags=""), timeout=TIMEOUT, verbose = 0)
	if (resp != None and resp.haslayer(TCP)):
		print "+(null scan)", ip, "port", port, str(resp.getlayer(TCP).flags), "\tping", (getms() - ms)
		return True
	return False
