from django.core.management.base import BaseCommand, CommandError

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Promotes the given user to a superuser and provides admin access."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, username, **options):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise CommandError(f"No user with username/email {username} found!")
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"{username} successfully promoted to superuser and can now access the admin site")
