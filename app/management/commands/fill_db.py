import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
from django.db import connection
class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'
    def delete_all(self):
        AnswerLike.objects.all().delete()
        QuestionLike.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE app_question_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE app_answer_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE app_tag_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;")
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
            User.objects.bulk_create(users)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(users)} пользователей'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания юзеров: {e}'))
        # Создание тегов
        try:
            tags = [Tag(title=f'tag{i}') for i in range(ratio)]
            Tag.objects.bulk_create(tags)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(tags)} тегов'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания тегов: {e}'))
        # Создание вопросов
        try:
            questions = []
            for i in range(ratio * 10):
                selected_tags = random.sample(tags, min(3, len(tags)))  # Выбираем 3 тега или меньше
                question = Question(
                    title=f'Вопрос {i}',
                    desc=f'Описание вопроса #{i}',
                    author=random.choice(users),
                )
                question.save()
                question.tags.set(selected_tags)  # Устанавливаем теги для вопроса
                questions.append(question)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(questions)} вопросов'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания вопросов: {e}'))
        # Создание ответов
        try:
            answers = []
            for i in range(ratio * 100):
                question = random.choice(questions)
                answer = Answer(
                    question=question,
                    author=random.choice(users),
                    content=f'Ответ на вопрос {question.title}'
                )
                answers.append(answer)
            Answer.objects.bulk_create(answers)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(answers)} ответов'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания ответов: {e}'))
        # Создание лайков для вопросов
        try:
            for question in questions:
                if random.random() < 0.5:  # 50% вероятность добавления лайка
                    QuestionLike.objects.create(
                        question=question,
                        user=random.choice(users)
                    )
            self.stdout.write(self.style.SUCCESS(f'Созданы лайки для вопросов'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания лайков для вопросов: {e}'))
        
        # Создание лайков для ответов
        try:
            for answer in answers:
                if random.random() < 0.5:  # 50% вероятность добавления лайка
                    AnswerLike.objects.create(
                        answer=answer,
                        user=random.choice(users)
                    )
            self.stdout.write(self.style.SUCCESS(f'Созданы лайки для ответов'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка создания лайков для ответов: {e}'))