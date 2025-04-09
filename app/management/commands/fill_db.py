import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like  # Импортируйте ваши модели
from django.db import connection
class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'
    def delete_all(self):
        Like.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE app_question_id_seq RESTART WITH 1;")
        self.stdout.write(self.style.SUCCESS(f'Удалены все старые объекты'))
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')
    def handle(self, *args, **options):
        ratio = options['ratio']
        try:
            self.delete_all()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка удаления старых данных: {e}'))
        # Создание пользователей
        try:
            users = [User(username=f'user{i}', password=str(i)) for i in range(ratio)]
            self.stdout.write(self.style.SUCCESS(f'Создано {len(users)} пользователей'))
            User.objects.bulk_create(users)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания юзеров: {e}'))
        # Создание тегов
        try:
            tags = [Tag(title=f'tag{i}') for i in range(ratio)]
            self.stdout.write(self.style.SUCCESS(f'Создано {len(tags)} тегов'))
            Tag.objects.bulk_create(tags)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания тегов: {e}'))
        # Создание вопросов
        try:
            questions=[]
            for i in range(ratio * 10):
        # Выбираем случайные 3 тега из всех тегов
                selected_tags = random.sample(tags, min(3, len(tags)))  # Выбираем 3 тега или меньше, если тегов меньше 3
                question = Question(
                title=f'Вопрос {i}',
                desc=f'Описание вопроса #{i}',
                author=random.choice(users)
                )
                question.save()
                question.tags.set(selected_tags)  # Устанавливаем теги для вопроса
                questions.append(question)
            
            
            self.stdout.write(self.style.SUCCESS(f'Создано {len(questions)} вопросов'))
            Question.objects.bulk_create(questions)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания вопросов: {e}'))
        # Создание ответов
        try:
            answers = [Answer(question=random.choice(questions),
                              author=random.choice(users),
                              content=f'Ответ на вопрос {i}') for i in range(ratio * 100)]
            self.stdout.write(self.style.SUCCESS(f'Создано {len(answers)} ответов'))
            Answer.objects.bulk_create(answers)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания ответов: {e}'))
        # Создание оценок
        try:
            likes = [Like(author=random.choice(users)) for i in range(ratio * 200)]
            self.stdout.write(self.style.SUCCESS(f'Создано {len(likes)} оценок'))
            Like.objects.bulk_create(likes)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания лайков: {e}'))