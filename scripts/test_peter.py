import thread
from heavy import *

ips = [ip_test]
senders = [None, "30.152.10.10"]

ports = []
for port in range(1, 10):
	ports.append(port)

for port in ports:
	for ip in ips:
		for send in senders:
			thread.start_new_thread(null_scan, (ip, 22,))
#			if syn_scan(ip, port, sender=send):
#				pass
#			else:
#				print " nothing on\t", ip, "\t", port, "\tfrom", send

print "+done sending"
time.sleep(4)
