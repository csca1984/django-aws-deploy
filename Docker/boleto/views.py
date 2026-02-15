from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static

from .models import Ticket, Complemetos
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.db import transaction
import random
from django.contrib.staticfiles import finders
import os
from django.db.models import Count
from django.db.models.functions import TruncDate

def index(request):
	"""Home page: render a simple landing page that uses the layout and shows the menu.

	This avoids redirecting — the root `/` will render `boletos.html` which extends `layout.html`.
	"""
	from .models import MenuItem
	menu_items = MenuItem.objects.filter(visible=True).order_by('order')
	# Render the boletos page (extends layout.html) so the layout and menu are visible at `/`
	return render(request, 'boleto/pages/boletos.html', {'menu_items': menu_items})


def page_view(request, slug):
	"""Render a page for the given slug. Template path: boleto/pages/<slug>.html"""
	from .models import MenuItem
	menu_items = MenuItem.objects.filter(visible=True).order_by('order')
	item = get_object_or_404(MenuItem, slug=slug)
	template_name = f'boleto/pages/{slug}.html'
	return render(request, template_name, {'menu_items': menu_items, 'item': item})


def sorteo_view(request):
	"""Mostrar formulario para generar N boletos y procesar la creación.

	POST: espera un campo `count` (int entre 1 y 1000). Crea N instancias `Ticket`
	y devuelve la lista de creados en la misma plantilla.
	"""
	from .models import MenuItem
	menu_items = MenuItem.objects.filter(visible=True).order_by('order')

	context = {'menu_items': menu_items}

	if request.method == 'POST':
		count_raw = request.POST.get('count')
		try:
			count = int(count_raw)
		except (TypeError, ValueError):
			context['error'] = 'Introduce un número válido.'
			return render(request, 'boleto/pages/sorteo.html', context)

		if count < 1 or count > 1000:
			context['error'] = 'El número debe estar entre 1 y 1000.'
			return render(request, 'boleto/pages/sorteo.html', context)

		if count < 1 or count > 1000:
			context['error'] = 'El número debe estar entre 1 y 1000.'
			return render(request, 'boleto/pages/sorteo.html', context)

		# Determinar número inicial: buscar máximo entero parseable en Ticket.number
		max_num = 0
		for val in Ticket.objects.values_list('number', flat=True):
			try:
				n = int(val)
				if n > max_num:
					max_num = n
			except Exception:
				continue

		start = max_num + 1

		# Prepare defaults from first Ticket if exists
		first = Ticket.objects.first()
		title = first.title if first else 'Komuna Baratza'
		message = first.message if first else 'Gracias por apoyar nuestra huerta comunitaria'
		date = first.date if first and first.date else None

		# Crear instancias
		to_create = []
		for i in range(count):
			num = str(start + i)
			to_create.append(Ticket(title=title, message=message, number=num, date=date))

		Ticket.objects.bulk_create(to_create)

		# Obtener los últimos creados (ordering por id)
		created = list(Ticket.objects.order_by('-id')[:count])[::-1]
		context['generated_tickets'] = created
		context['count'] = count

		return render(request, 'boleto/pages/sorteo.html', context)

	# Para GET u otros métodos, renderizamos la plantilla con el formulario vacío/contexto
	return render(request, 'boleto/pages/sorteo.html', context)


def boletos_view(request):
	"""Página de 'Boletos' que también permite generar N boletos vía POST.

	Reusa la misma lógica que `sorteo_view` pero renderiza `pages/boletos.html`.
	"""
	from .models import MenuItem
	menu_items = MenuItem.objects.filter(visible=True).order_by('order')

	context = {'menu_items': menu_items}

	if request.method == 'POST':
		count_raw = request.POST.get('count')
		try:
			count = int(count_raw)
		except (TypeError, ValueError):
			context['error'] = 'Introduce un número válido.'
			return render(request, 'boleto/pages/boletos.html', context)

		if count < 1 or count > 1000:
			context['error'] = 'El número debe estar entre 1 y 1000.'
			return render(request, 'boleto/pages/boletos.html', context)

		# Prepare defaults from first Ticket if exists
		complementos_obj = Complemetos.objects.first()
		title = complementos_obj.title if complementos_obj else 'Komuna Baratza'
		message =complementos_obj.message if complementos_obj else 'Gracias por apoyar nuestra huerta comunitaria'
		fecha =complementos_obj.date if complementos_obj else '2025-12-25'		
		precio =complementos_obj.precio if complementos_obj else '5Є'

		# Crear instancias
		with transaction.atomic():
			last_ticket = Ticket.objects.order_by('-number').first()
			start_num = last_ticket.number + 1 if last_ticket else 1
			start = last_ticket.number + 1 if last_ticket else 1
			to_create = []
			for i in range(count):
				num = str(start + i)
				to_create.append(Ticket( number=num))

		Ticket.objects.bulk_create(to_create)

		
		#context['generated_tickets'] = to_create
		#context['count'] = count

		context.update({
            'generated_tickets': to_create,
            'count': count,
            'title': title,
            'message': message,
			'date': fecha,
			'precio': precio,
        })

		return render(request, 'boleto/pages/boletos.html', context)

	return render(request, 'boleto/pages/boletos.html', context)


def download_tickets_pdf(request):

	if request.method != 'POST':
		return HttpResponseBadRequest('POST required')

	ids = request.POST.getlist('ids')
	if not ids:
		return HttpResponseBadRequest('No ticket ids provided')

	tickets_qs = Ticket.objects.filter(pk__in=ids)

	id_to_ticket = {str(t.pk): t for t in tickets_qs}
	tickets = [id_to_ticket[i] for i in ids if i in id_to_ticket]

	#Complementos
	complementos_obj = Complemetos.objects.first()
	title = complementos_obj.title if complementos_obj else 'Komuna Baratza'
	message =complementos_obj.message if complementos_obj else 'Gracias por apoyar nuestra huerta comunitaria'
	fecha =complementos_obj.date if complementos_obj else '2025-12-25'
	precio =complementos_obj.precio if complementos_obj else '5Є'
	#fin de complementos

	##################IMAGEN#################3
    # Ruta local de la imagen
	image_path = finders.find('boleto/images/goteo.jpeg')  # Busca el archivo en STATICFILES
	if not image_path:
		return HttpResponseBadRequest('Imagen no encontrada en static files')
	image_url = f'file://{os.path.abspath(image_path)}'  # Ruta absoluta en formato file://
	##################IMAGEN###################

	##################CSS###################
	css_path = finders.find('boleto/css/ticket.css')
	if not css_path:
		return HttpResponseBadRequest('CSS no encontrado')
	css_url = f'file://{os.path.abspath(css_path)}'
	##################CSS###################
	# Render HTML for the tickets (we'll reuse the boletos template but a PDF-specific one)
	from django.template.loader import render_to_string
	# Use a clean template (no layout) optimized for PDF printing
	#static_root = '/app/static/'
	

	#image_url = request.build_absolute_uri(static('boleto/images/goteo.jpeg'))
	html_string = render_to_string('boleto/pages/boletos_pdf_clean.html', {
		'generated_tickets': tickets,
		'title': title,
        'message': message,
		'date': fecha,
		'precio': precio,
		'image_url': image_url,
		'css_url': css_url,
	}, request=request)

	# Build filename with daymonthyear
	from datetime import datetime
	dt = datetime.now()
	fname = f"sorte_baratza_{dt.day:02d}{dt.month:02d}{dt.year}.pdf"

	try:
		from weasyprint import HTML
	except Exception:
		# WeasyPrint not installed: return the clean HTML page so user can print/save manually
		return render(request, 'boleto/pages/boletos_pdf_clean.html', {'generated_tickets': tickets})

	# Generate PDF using WeasyPrint
	base_url = request.build_absolute_uri('/')
	pdf = HTML(string=html_string, base_url=base_url).write_pdf()

	from django.http import HttpResponse
	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename="{fname}"'
	return response


def generar_ganador(request):
    tickets = Ticket.objects.filter(sorteo=True).values_list('number', flat=True)
    ticket_seleccionado = None
    if tickets:
        ticket_seleccionado = random.choice(list(tickets))


    complementos_obj = Complemetos.objects.first()
    title = complementos_obj.title if complementos_obj else 'Komuna Baratza'
    message = complementos_obj.message if complementos_obj else 'Gracias por apoyar nuestra huerta comunitaria'
    fecha = complementos_obj.date if complementos_obj else '2025-12-25'
    precio = complementos_obj.precio if complementos_obj else '5€'

    # Aquí puedes devolver una respuesta o render
    return render(request, "boleto/pages/boleto_ganador.html", {
        "ganador": ticket_seleccionado,
        "title": title,
        "message": message,
        "fecha": fecha,
        "precio": precio,
		"hay_ganador": ticket_seleccionado is not None,
    })


def dashboard(request):
    # Boletos que entran en el sorteo
    tickets_sorteo = Ticket.objects.filter(sorteo=True)

    # Boletos que NO entran en el sorteo
    tickets_no_sorteo = Ticket.objects.filter(sorteo=False)

    # Boletos vendidos por día
    boletos_por_dia = (
        tickets_sorteo
        .annotate(fecha=TruncDate('creado'))
        .values('fecha')
        .annotate(total=Count('id'))
        .order_by('fecha')
    )

    # Totales
    total_vendidos = tickets_sorteo.count()
    total_ganado = total_vendidos * 5

    context = {
        'tickets_sorteo': tickets_sorteo,
        'tickets_no_sorteo': tickets_no_sorteo,
        'boletos_por_dia': boletos_por_dia,
        'total_vendidos': total_vendidos,
        'total_ganado': total_ganado,
    }
    return render(request, "boleto/pages/dashboard.html", context)