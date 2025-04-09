import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like  # Импортируйте ваши модели
class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'
    def delete_all(self):
        Like.objects.all().delete();
        Tag.objects.all().delete();
        User.objects.all().delete();
        Question.objects.all().delete();
        Answer.objects.all().delete();
        self.stdout.write(self.style.SUCCESS(f'Удалены все старые объекты'))
        
    
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')
    def handle(self, *args, **options):
        ratio = options['ratio']

        self.delete_all()
        # Создание пользователей

        users = [User(username=f'user{i}', password=str(i)) for i in range(ratio)]
    
        self.stdout.write(self.style.SUCCESS(f'Создано {len(users)} пользователей'))
        User.objects.bulk_create(users)
        # Создание тегов
        
        tags = [Tag(title=f'tag{i}') for i in range(ratio)]
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(tags)} тегов'))
        Tag.objects.bulk_create(tags)
        # Создание вопросов
        
        questions = [Question(title=f'Вопрос {i}',author=random.choice(users)) for i in range(ratio * 10)]

        self.stdout.write(self.style.SUCCESS(f'Создано {len(questions)} вопросов'))
        Question.objects.bulk_create(questions)
        # Создание ответов

        answers = [Answer(question=random.choice(questions),
                author=random.choice(users),
                content=f'Ответ на вопрос {i}') for i in range(ratio * 100)]
        

        self.stdout.write(self.style.SUCCESS(f'Создано {len(answers)} ответов'))
        Answer.objects.bulk_create(answers)
        # Создание оценок
        
        likes = [Like(author=random.choice(users)) for i in range(ratio * 200)]
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(likes)} оценок'))
        Like.objects.bulk_create(likes)