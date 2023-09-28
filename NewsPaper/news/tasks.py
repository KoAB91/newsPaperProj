import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category


@shared_task()
def send_new_posts():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True)
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task()
def send_notifications(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.category.all()
    subscribers = []
    for category in categories:
        subscribers += category.subscribers.all()
    subscribers = [s.email for s in subscribers]

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.email_preview,
            'link': f'{settings.SITE_URL}/news/{post_id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
