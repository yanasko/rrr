from celery import shared_task
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def crazy(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    preview = post.preview()
    subscribers_emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]
        #for sub in subscribers:
            #subscribers_emails.append(sub.email)

        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/post/{pk}'  # posts
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers_emails,
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def week_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_create__gte=last_week)

    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

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
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
