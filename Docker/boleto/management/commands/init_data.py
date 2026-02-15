from django.core.management.base import BaseCommand
from boleto.models import MenuItem

class Command(BaseCommand):
    help = "Inicializa datos básicos de la aplicación"

    def handle(self, *args, **options):
        menu_items = [
            {
                "pk": 1,
                "name": "Normas",
                "slug": "normas",
                "visible": True,
                "order": 1,
            },
            {
                "pk": 2,
                "name": "Boletos",
                "slug": "boletos",
                "visible": True,
                "order": 2,
            },
            {
                "pk": 3,
                "name": "Sorteo",
                "slug": "sorteo",
                "visible": False,
                "order": 3,
            },
            {
                "pk": 4,
                "name": "Resultados",
                "slug": "resultados",
                "visible": True,
                "order": 4,
            },
        ]

        for item in menu_items:
            obj, created = MenuItem.objects.update_or_create(
                pk=item["pk"],
                defaults={
                    "name": item["name"],
                    "slug": item["slug"],
                    "visible": item["visible"],
                    "order": item["order"],
                },
            )

            action = "Creado" if created else "Actualizado"
            self.stdout.write(
                self.style.SUCCESS(f"{action} MenuItem: {obj.name}")
            )

        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados correctamente"))
