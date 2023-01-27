# Данный файл утратил свое значение после подключения к проекту Celery and Redis
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
#
# from .models import PostCategory
# from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL
#
#
# def send_notifications(preview, pk, title, subscribers, id):
#     mailing_list = list(PostCategory.objects.filter(postThrough_id=id).values_list(
#         'categoryTrough__subscribers__username',
#         'categoryTrough__subscribers__first_name',
#         'categoryTrough__subscribers__email',
#         'categoryTrough__name',
#         )
#     )
#     for client, first_name, email, category in mailing_list:
#         html_content = render_to_string(
#             'post_created_email.html',
#             {
#                 'text': preview,
#                 'link': f'{SITE_URL}/news/{pk}',
#                 'client': client,
#                 'category': category,
#             }
#         )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.postCategory.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers, instance.id)