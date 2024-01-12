from django.core.management import BaseCommand

from django.contrib.auth.models import User


def add_users():
    User.objects.create_user(username='user1', email='user1@user.com', password='1234')
    User.objects.create_user(username='user2', email='user2@user.com', password='1234')
    User.objects.create_user(username='user3', email='user3@user.com', password='1234')
    User.objects.create_superuser(username='root', email='root@root.com', password='1234')
    User.objects.create_superuser(username='root2', email='root2@root.com', password='1234')
    User.objects.create_superuser(username='root3', email='root3@root.com', password='1234')

    print("Пользователи созданы")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()

