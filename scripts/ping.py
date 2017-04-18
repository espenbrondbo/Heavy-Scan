from scapy.all import *
from utils import *

def ping(ip, bytes=0, tries=2):
	global TIMEOUT
	
	times = []
	pings = tries
	
	if bytes > 65500:
		bytes = 65500
		
	data = "x" * bytes
	for i in range(0, pings):
		packet = IP(dst=ip)/ICMP()/data
		
		ms = getms()

		resp = sr1(packet, verbose=0, timeout=TIMEOUT)

		if resp != None:
			times.append(getms() - ms)
	
	answer = False
	for i in times:
		if i != 0:
			answer = True
	if not answer:
		p = "-no response from " + ip
		#print p
		return
		
	maxim, minim, avg = 0, 100000000, 0
	
	for time in times:
		if time > maxim:
			maxim = time
		if time < minim:
			minim = time
		avg += time
	avg /= pings
	out = ("+ping " + ip + "  \tmax " + str(maxim) + "ms  min " + str(minim) + 
			"ms  average " + str(avg) + "ms  " + str(bytes) + "bytes")
	print out
