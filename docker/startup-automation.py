import os

from django.contrib.auth.models import User

if not User.objects.filter(
    username=os.environ["DJANGO_DEFAULT_ADMIN_USERNAME"]
).exists():
    """Creates a default Django admin account"""

    u = User(username=os.environ["DJANGO_DEFAULT_ADMIN_USERNAME"])
    u.set_password(os.environ["DJANGO_DEFAULT_ADMIN_PASSWORD"])
    u.is_superuser = True
    u.is_staff = True
    u.save()
    u = User.objects.get(username=os.environ["DJANGO_DEFAULT_ADMIN_USERNAME"])
    u.save()
    print("Successfully created admin account.")
