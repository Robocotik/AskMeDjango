from django.core.management.base import BaseCommand
from django.core.cache import cache
from app.models import Tag, User

class Command(BaseCommand):
    help = 'Update cache for popular tags and top users'

    def handle(self, *args, **options):
        
        tags = Tag.objects.popular_tags()
        self.stdout.write(f'Updated cache for {len(tags)} popular tags')
        
        
        users = User.objects.top_users()
        self.stdout.write(f'Updated cache for {len(users)} top users')