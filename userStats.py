class UserStats:
	def __init__(self,d=None,amor=0,animo=0,energia=0,hot=0):
		if(d):
			self.amor = d['amor']
			self.animo = d['animo']
			self.energia = d['energia']
			self.hot = d['hot']
		else:			
			self.amor = amor
			self.animo = animo
			self.energia = energia
			self.hot = hot
	def test(self,amor,animo,energia,hot):
		ramor = self.amor-amor
		ranimo = self.animo-animo
		renergia = self.energia-energia
		rhot = self.hot-hot
		if(ramor < 0 or ranimo < 0 or renergia < 0 or rhot < 0):
			return False
		else:
			self.amor = ramor
			self.anime = ranimo
			self.energia = renergia
			self.hot = rhot 
			return True