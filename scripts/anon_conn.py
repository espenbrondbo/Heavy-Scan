from utils import *
from syn_scan import *
import ftplib


def anon_conn(ip):
	global TIMEOUT

	print "start " + ip
	nttl = random.randint(99, 144)
	
	#simple syn-scan, to see if port is open
	resp = sr1(IP(dst=ip, ttl=nttl)/TCP(dport=21, flags="S"), timeout=TIMEOUT, verbose=0)
	
	if resp is not None and resp.getlayer(TCP):
		if resp.getlayer(TCP).flags == 18 and resp.getlayer(TCP):
			try:
				ftp = ftplib.FTP(ip)
				ftp.login()
#				ftp.retrlines('list')
				welcome = '+(anoncon) ' + ip + " \t" + ftp.getwelcome()
				ftp.close()
				print welcome
				return True
			except:
				print " (anoncon) incorrect login @" + ip
		
	#print " anonconn", ip
	return False
