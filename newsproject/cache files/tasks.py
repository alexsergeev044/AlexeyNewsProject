from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Post, Category, Mailing


# Реализовать рассылку уведомлений подписчикам после создания новости.
@shared_task
def send_msg(category, post_title, post_type, post_url, emails):
    subject = f'Новая публикация в категории {category}'

    text_content = (
        f'Название: {post_title}\n'
        f'Тип: {post_type}\n'
        f'Категория: {category}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1:8000{post_url}'
    )
    html_content = (
        f'Название: {post_title}<br>'
        f'Тип: {post_type}<br>'
        f'Категория: {category}<br><br>'
        f'<a href="http://127.0.0.1:8000{post_url}">'
        f'Ссылка на публикацию</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# Реализовать еженедельную рассылку с последними новостями.
@shared_task
def news_send():
    bulk_list = []
    for user in User.objects.exclude(email__isnull=True).exclude(email=''):

        user_category = Category.objects.filter(pk__in=user.subscriptions.all().values_list('category', flat=True))
        user_cat_str = '|'.join(user_category.values_list('category_name', flat=True))

        request_period = datetime.now() - timedelta(days=14)

        news = Post.objects.exclude(mailings__user=user).filter(
            post_category__in=user_category,
            post_date__gte=request_period
        ).distinct().order_by('-post_date')

        if len(news) > 0:

            subject = f'Новые публикации в категории {user_cat_str}'
            text_content = f'Новые публикации в категории {user_cat_str}:\n'
            html_content = f'Новые публикации в категории {user_cat_str}:<br>'
            n = 0
            for p in news:
                n += 1
                category_str = '|'.join(p.post_category.all().values_list('category_name', flat=True))
                text_content += (
                    f'{n}) {p.get_post_type_display()} - '
                    f'{p.post_title} '
                    f'({category_str}) - '
                    f'http://127.0.0.1:8000{p.get_absolute_url()}\n'
                )
                html_content += (
                    f'{n}) {p.get_post_type_display()} - '
                    f'<a href="http://127.0.0.1:8000{p.get_absolute_url()}">{p.post_title}</a> '
                    f'({category_str})<br>'
                )
                bulk_list.append(Mailing(user=user, post=p))

            msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    Mailing.objects.bulk_create(bulk_list)