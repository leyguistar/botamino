class Player:

	def __init__(self,id,nombre,descripcion,estado,lugar,ficha):
		self.id = id
		self.nombre = nombre
		self.descripcion = descripcion
		self.estado = estado
		self.lugar = lugar
		self.felidad = 0
		self.salud = 0
		self.pensamiento = ""
		self.accion = ""

		