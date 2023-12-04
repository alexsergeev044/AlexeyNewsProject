from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, PostCategory
from .tasks import send_msg


@receiver(post_save, sender=PostCategory)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = list(User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True).distinct())

    if len(emails) > 0:
        send_msg.delay(instance.category.category_name, instance.post.post_title,
                       instance.post.get_post_type_display(), instance.post.get_absolute_url(), emails)


@receiver(m2m_changed, sender=Post.post_category.through)
def category_saved(instance, action, **kwargs):
    if action != 'post_add':
        return

    category_str = '|'.join(instance.post_category.all().values_list('category_name', flat=True))

    emails = list(User.objects.filter(
        subscriptions__category__in=instance.post_category.all()
    ).values_list('email', flat=True).distinct())

    if len(emails) > 0:
        send_msg.delay(category_str, instance.post_title, instance.get_post_type_display(),
                       instance.get_absolute_url(), emails)