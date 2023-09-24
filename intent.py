class Intent():
	def __init__(self,secuency):
		self.secuency = secuency
		self.state = {}
		
	def next(self,userid):
		if(userid in self.state):
			if(self.state[userid][0]+1 >= len(self.secuency)):
				self.state.pop(userid)
			else:
				self.state[userid][0] += 1
				self.state[userid][1] = 1
		else:
			if(len(self.secuency) > 1):
				self.state[userid] = [1,1]
	def get(self,userid):
		state = self.state.get(userid,[0,0] )
		if(state[0] and state[1] > 3):
			self.state.pop(userid)
		else:
			state[1] += 1
		return self.secuency[state[0]]
	def reset(self):
		self.state = 0