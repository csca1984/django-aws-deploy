from django.contrib import admin
from .models import Ticket, Complemetos


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ('number','sorteo','creado')
	list_editable = ('sorteo',)
	list_filter = ('creado',)
	search_fields = ('number','sorteo','creado')
	#ordering = ('-id',)
	ordering = ('-creado',)

@admin.register(Complemetos)
class ComplemetosAdmin(admin.ModelAdmin):
	list_display = ('title','message','date')
	search_fields = ('title','message','date',)
	ordering = ('-id',)

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'visible', 'order')
	list_editable = ('visible', 'order')
	prepopulated_fields = {'slug': ('name',)}
	ordering = ('order',)

