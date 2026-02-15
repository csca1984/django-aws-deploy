from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Complemetos

@receiver(post_migrate)
def create_default_complementos(sender, **kwargs):
    # Evita que se ejecute para todas las apps
    if sender.name != 'boleto':
        return

    # Si no existe ningún registro, crea uno
    if not Complemetos.objects.exists():
        Complemetos.objects.create(
            title='Komuna Baratza',
            message='Gracias por apoyar nuestra huerta comunitaria',
            date=None
        )
        print("✅ Registro por defecto de Complemetos creado.")