from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Sets up Admin group and adds users to it'

    def handle(self, *args, **kwargs):
        # Create Admin group if it doesn't exist
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admin group'))
        
        # Add all users to Admin group
        users = User.objects.all()
        for user in users:
            if not user.groups.filter(name='Admin').exists():
                user.groups.add(admin_group)
                self.stdout.write(self.style.SUCCESS(f'Added {user.username} to Admin group'))
        
        self.stdout.write(self.style.SUCCESS('Successfully set up admin permissions')) 