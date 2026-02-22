import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Create a superuser from environment variables if one does not exist. "
        "Reads DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL (optional), "
        "and DJANGO_SUPERUSER_PASSWORD. Idempotent: does nothing if the user "
        "already exists."
    )

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stderr.write(
                "DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD "
                "must be set. Skipping superuser creation."
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                f"Superuser '{username}' already exists. Skipping."
            )
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        except Exception as exc:
            raise CommandError(
                f"Failed to create superuser '{username}': {exc}"
            ) from exc

        self.stdout.write(
            self.style.SUCCESS(f"Superuser '{username}' created successfully.")
        )
