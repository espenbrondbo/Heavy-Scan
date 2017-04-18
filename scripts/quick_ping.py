from utils import *
from scapy.all import *

def quick_ping(ip):
	global TIMEOUT
	
	packet = IP(dst=ip)/ICMP()

	resp = sr1(packet, verbose = 0, timeout = TIMEOUT)

	if (resp != None):
		print "+confirming " + ip
		return True
	return False
