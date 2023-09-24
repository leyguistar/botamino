class Comunidad:

	def __init__(self,id,botid=None,wallMessage='',privateChatMessage='',recibir=0,welcomeChat=None,welcomeChatMessage=None,bots=1):
		self.id = id
		self.wallMessage = wallMessage
		self.privateChatMessage = privateChatMessage
		self.recibir = recibir
		self.botid = botid
		self.welcomeChat = welcomeChat
		self.welcomeChatMessage= welcomeChatMessage
		self.bots = bots
		self.idioma = None
		self.miembros = None