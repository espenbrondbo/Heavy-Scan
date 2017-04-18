from scapy.all import *
from heavy import *
import socket

def get_header(ip, port):
	global TIMEOUT
	
#	print " get header", ip, port
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(TIMEOUT)
		s.connect((ip, port))
		if port is 80: #HTTP server
			s.send("GET / HTTP/1.0\r\n\r\n")
			
		data = str(s.recv(1000))
		
		if port is 80: #HTTP server, need to cut out the html
			lines = data.split("\n")
			header = "\t"
			for line in lines:
				if "<html" in line or "<HTML" in line:
					break # we don't want the code for the site, only headers
				if len(line) > 1:
					header += line + "\n\t"
				if "Server:" in line:
					server = line.replace("Server:", "")
			print ("+header from " + ip + ":" + str(port) + " \n" + header[:-2])
		else: #not HTTP server
			if data:
				data = data.replace("\n", "")
				print ("+header from " + ip + ":" + str(port) + " \t" + data)
		s.close()
		return True
		
	except:
		pass
#		print ("-error getting header from " + ip + ":" + str(port))
	return False

	nttl = random.randint(99, 144)
	ipp = IP(dst=ip, ttl=nttl)
	seqnr = random.randint(1034245, 3034245)
	tpac = TCP(dport=port, flags="S", seq = seqnr)
	synack = sr1(ipp/tpac, timeout=TIMEOUT, verbose = 0)
	
	if synack != None and synack.getlayer(TCP):
		tcp = synack.getlayer(TCP)
#		print "flags " + str(tcp.flags)
#		print synack
		if tcp.flags != 18:
			return False
		print ("##seq" + str(synack.seq))
			
		tcpack = TCP(dport = port, flags="A", seq = seqnr + 1, ack = synack.seq + 1)
		
		resp = sr1(ipp/tcpack, timeout=TIMEOUT, verbose = 0)
		
		if resp != None:
			print ("##response " + ip + ":" + str(port) + " " + resp)
		else:
			print ("##no response " + ip + ":" + str(port))
	elif synack != None:
		print " wtf at:" + ip + ":" + str(port)
		synack.show()
	return False
	
