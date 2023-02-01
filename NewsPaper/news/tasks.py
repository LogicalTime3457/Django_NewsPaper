import logging

import datetime

from celery import shared_task


from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django_apscheduler.models import DjangoJobExecution
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

from .models import PostCategory, Post, Category
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL, TIME_ZONE


@shared_task
def send_notifications(preview, pk, title, subscribers, id):
    mailing_list = list(PostCategory.objects.filter(postThrough_id=id).values_list(
        'categoryTrough__subscribers__username',
        'categoryTrough__subscribers__first_name',
        'categoryTrough__subscribers__email',
        'categoryTrough__name',
        )
    )
    for client, first_name, email, category in mailing_list:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f'{SITE_URL}/news/{pk}',
                'client': client,
                'category': category,
            }
        )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers, instance.id)


@shared_task
def mailing_weekly():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
            'daily_post.html',
            {
                'link': SITE_URL,
                'posts': posts,
            }
        )
    msg = EmailMultiAlternatives(
        subject='News on week',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()



