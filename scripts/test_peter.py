from heavy import *

#addresses to scan
ips = ["209.85.128.0", "209.85.128.1", "209.85.128.2"]

#addresses to make it look like scan came from (None is normal IP)
senders = [None, "4.4.4.4"]

#ports to scan
ports = [21, 80, 441]

#scan loop
for port in ports:
	for ip in ips:
		for sender in senders:
			#make scan look like its coming from somewhere else
			if syn_scan(ip, port, sender=sender):
				print " hit on \t", ip, "\t", port, "\tfrom", sender
				if sender is None:
					#only print header if scan was from this ip
					get_header(ip, port)
			else:
				print " nothing on\t", ip, "\t", port, "\tfrom", sender

print "+done sending"

#wait for all requests to complete or time out
time.sleep(4)
