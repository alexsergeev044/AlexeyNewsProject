from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда позволяет удалять все публикации из какой-либо категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все публикации в категории {options["category"]}? да/нет')

        if answer != 'да':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(post_category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все публикации в категории {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти публикации в категории {options["category"]}'))