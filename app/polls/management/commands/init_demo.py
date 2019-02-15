import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from polls.models import Question, Choice


class Command(BaseCommand):
    help = 'Load initial demo data to the application'

    @staticmethod
    def create_super_user():
        User.objects.create_superuser(
            username='demo',
            email="demo@example.com",
            password='demo'
        )

    @staticmethod
    def create_demo_polls():
        polls = {
            'Django vs Flask': [
                'Django',
                'Flask'
            ],
            'Python vs Ruby': [
                'Python',
                'Ruby'
            ],
        }

        for question_text, choices in polls.items():
            question = Question.objects.create(
                question_text=question_text,
                pub_date=now()
            )

            for choice_text in choices:
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text
                )

    @staticmethod
    def already_initialized():
        if User.objects.filter(username='demo').exists():
            return True

        return False

    def handle(self, *args, **options):
        if os.environ.get('INIT_DEMO') != 'True':
            return

        if self.already_initialized():
            self.stdout.write(self.style.SUCCESS('Already initialized'))
            return

        self.create_super_user()
        self.create_demo_polls()

        self.stdout.write(self.style.SUCCESS('Successfully init poll demo'))
