from django.db.models.signals import post_migrate
from main.models import User
from django.dispatch import receiver

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    if not User.objects.filter(email='admin@gmail.com').exists():
        User.objects.create_superuser(email='admin@gmail.com', password='admin')

