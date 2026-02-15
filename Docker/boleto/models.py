from django.db import models


class Ticket(models.Model):
	"""Modelo que almacena los valores mostrados en la plantilla del boleto.
	Campos:
	- number: número del boleto (numero secuencial)
	- sorteo: si el boleto ha sido sorteado
	- creado: fecha de creacion del boleto	
	"""
	number = models.PositiveIntegerField(unique=True,blank=True, help_text='Número del boleto')
	sorteo = models.BooleanField(default=False)
	creado = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Boleto'
		verbose_name_plural = 'Boletos'
		ordering = ['-id']

	def __str__(self) -> str:
		return f" #{self.number}"


class Complemetos(models.Model):

	title = models.CharField(max_length=200, default='Komuna Baratza')
	message = models.TextField(blank=True, default='Gracias por apoyar nuestra huerta comunitaria')
	date = models.DateField(blank=True, null=True, help_text='Fecha del sorteo')
	precio = models.CharField(max_length=200,null=True,blank=True, help_text='el precio del boleto')

	class Meta:
		verbose_name = 'Complentos'
		verbose_name_plural = 'Complentos'
		ordering = ['-id']

	def __str__(self) -> str:
		return f"{self.title}"




class MenuItem(models.Model):

	name = models.CharField(max_length=100, help_text='Texto que se muestra en el menú')
	slug = models.SlugField(max_length=100, unique=True)
	visible = models.BooleanField(default=True)
	order = models.IntegerField(default=0, help_text='Orden en el menú (asc)')

	class Meta:
		verbose_name = 'Elemento de menú'
		verbose_name_plural = 'Elementos de menú'
		ordering = ['order', 'id']

	def __str__(self) -> str:
		return self.name


