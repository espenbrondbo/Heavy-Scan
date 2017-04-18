import thread, time

NOTHING = 0
BUSY = 1

	

class ThreadPool:
	
	def __init__(self, cap, jobstats = 2000):
		self.cap = cap
		self.arr = []
		self.jobnum = 0
		self.jobstats = jobstats
		for i in range(0, cap + 1):
			self.arr.append(NOTHING)
	
	def addjob(self, fun, args):
		hasthread = False
		tid = -1
		
		self.jobnum += 1
		if self.jobstats != 0 and self.jobnum % self.jobstats == 0:
			f = str(fun)
			f = f.replace("<function ", "")
			f = f[0: f.find(" at 0x")]
			p = (" job " + str(self.jobnum) + " \t" + f + " \t" + str(args))
			print p
		
		while not hasthread:
			for i in range(0, len(self.arr)):
				if self.arr[i] == NOTHING:
					hasthread = True
					tid = i
					break
			if not hasthread:
				try:
					time.sleep(0.05)
				except:
					pass
		try:
			time.sleep(0.1)
		except:
			pass
		thread.start_new_thread(self.poollauncher, (fun, args, tid))
		
	def poollauncher(self, fun, args, tid):
		self.arr[tid] = BUSY
		
		try:
			fun(*args)
		except:
			pass
		
		self.arr[tid] = NOTHING
		
	def hasmorejobs(self):
		ret = False
		
		for status in self.arr:
			if status == BUSY:
				ret = True
		
		return ret
