from scapy.all import *
from utils import *


def connection_scan(ip, port):
	global TIMEOUT
	#print "scanning", ip, port
	
	try:
		s = socket.socket(socket.AF_INET,
						  socket.SOCK_STREAM)
		s.settimeout(TIMEOUT)
		response = s.connect_ex((ip, port))
		s.close()
	
		if response == 0:
			print "+(pingscan) ", ip, port
			return True
	except socket.error:
		print "-error"
	return False
