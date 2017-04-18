from scapy.all import *
from utils import *


def udp_scan(ip, port, sender=None):
	global TIMEOUT
	
	resp = sr1(IP()/UDP(), verbose=0, timeout=TIMEOUT)
	if resp.haslayer(UDP):
		return True
	elif resp.haslayer(ICMP):
		print " ICMP response from port", port
#		resp.show()
	else:
		print "nothing from port", port
	return False
