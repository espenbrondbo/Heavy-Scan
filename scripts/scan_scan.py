from heavy import *
import sys

pool = ThreadPool(8)

if len(sys.argv) == 1:
	print "Usage: " + sys.argv[0] + "<-i ipfile> <-p portfile> <-s senderfile> <args>"
	print "\t-Ss\tSyn scan"
	print "\t-Sc\tConnection scan"
	print "\t-Sn\tNull scan"
	print "\t-Su\tUDP scan"
	print "\t-P\tPing"
	print "\t\t-Pb\tBytes to send ping"
	print "\t\t-Pt\tPings to send each host"
	print "\t\t-Pq\tQuick ping"
	print "\t-Gh\tGet header from port"
	print "\t-Ca\tAttempt to connect anonymously to FTP (port 21)"
	print "\n"
	print "\t-i ipfile | file with a list of (line seperated) adresses to scan/ping"
	print "\t-p portfile | file with a list of (line seperated) ports to scan"
	print "\t-s senderfile | file with a list of (line seperated) IPs to send from (only for syn scan)"

ipfile = portfile = senderfile = ""
pingbytes = pingtries = 10
pingscan = synscan = connscan = nullscan = udpscan = anonconn = quickping = getheader = False
ips = []
ports = []
senders = []

for i in range (1, len(sys.argv)):
	arg = sys.argv[i]
	if arg == '-i':
		ipfile = sys.argv[i + 1]
	if arg == '-p':
		portfile = sys.argv[i + 1]
	if arg == '-s':
		senderfile = sys.argv[i + 1]
	if arg == '-Pt':
		pingtries = int(sys.argv[i + 1])
	if arg == '-Ca':
		anonconn = True
	if arg == "-Ss":
		synscan = True
	if arg == "-Sc":
		connscan = True
	if arg == "-Sn":
		nullscan = True
	if arg == "-Su":
		udpscan = True
	if arg == "-P":
		pingscan = True
	if arg == '-Pq':
		quickping = True
	if arg == '-Gh':
		getheader = True
	if arg == "-Pb":
		pingbytes = int(sys.argv[i + 1])

def parse_ip_range(inp):
	ret = []
	cur = ""
	number = 0
	fromnum = 0
	inrange = False
	parts = inp.split(".")
	astart = aend = 0
	bstart = bend = 0
	cstart = cend = 0
	dstart = dend = 0
	
	if len(parts) != 4:
		return inp
	
	for ch in parts[0]:
		if ch in "1234567890":
			number *= 10
			number += int(ch)
		elif ch in "-":
			inrange = True
			fromnum = number
			number = 0
	if inrange:
		astart = fromnum
		aend = number + 1
	else:
		astart = number
		aend = number + 1
	inrange = False
	number = 0
	for ch in parts[1]:
		if ch in "1234567890":
			number *= 10
			number += int(ch)
		elif ch in "-":
			inrange = True
			fromnum = number
			number = 0
	if inrange:
		bstart = fromnum
		bend = number + 1
	else:
		bstart = number
		bend = number + 1
	
	inrange = False
	number = 0
	for ch in parts[2]:
		if ch in "1234567890":
			number *= 10
			number += int(ch)
		elif ch in "-":
			inrange = True
			fromnum = number
			number = 0
	if inrange:
		cstart = fromnum
		cend = number + 1
	else:
		cstart = number
		cend = number + 1
	inrange = False
	number = 0
	for ch in parts[3]:
		if ch in "1234567890":
			number *= 10
			number += int(ch)
		elif ch in "-":
			inrange = True
			fromnum = number
			number = 0
	if inrange:
		dstart = fromnum
		dend = number + 1
	else:
		dstart = number
		dend = number + 1
	
	
	for a in range(astart, aend):
		for b in range(bstart, bend):
			for c in range(cstart, cend):
				for d in range(dstart, dend):
					ret.append(str(str(a) + "." + str(b) + "." + str(c) + "." + str(d)))
	return ret

if ipfile:
	with open(ipfile) as f:
		for ip in f.readlines():
			ip = ip.replace("\n", "")
			if len(ip) > 4:
#				print " ip\t", ip
				for i in parse_ip_range(ip):
#					print " ", i
					ips.append(i)
					
if portfile:
	with open(portfile) as f:
		for port in f.readlines():
			port = port.replace("\n", "")
#			print " port\t", port
#			if len(port) > 0:
#				for p in parse_range(int(port)):
#					ports.append(p)
			for p in parse_range(port):
				ports.append(p)
#			ports.append(int(port))

if senderfile:
	with open(senderfile) as f:
		for sender in f.readlines():
			sender = sender.replace("\n", "")
			if len(sender) > 0:
				if sender == "None":
					senders.append(None)
				else:
					senders.append(sender)

if quickping:
	for ip in ips:
		pool.addjob(quick_ping, (ip,))

if pingscan:
	for ip in ips:
#		print "+to ping", ip, bytes
		pool.addjob(ping, (ip, pingbytes, pingtries))
		
if getheader:
	for ip in ips:
		for port in ports:
			pool.addjob(get_header, (ip, port))
#			get_header(ip, port)

if nullscan:
	for ip in ips:
		for port in ports:
			pool.addjob(null_scan, (ip, port))
if synscan:
	for ip in ips:
		for port in ports:
			if senders:
				for client in senders:
					pool.addjob(syn_scan, (ip, port, client))
			else:
				pool.addjob(syn_scan, (ip, port))

if anonconn:
	for ip in ips:
		pool.addjob(anon_conn, (ip,))
#		anon_conn(ip)

while pool.hasmorejobs():
	try:
		time.sleep(0.2)
	except:
		pass

try:
	time.sleep(1)
except:
	pass
	
print "All", pool.jobnum, "scans complete!"
