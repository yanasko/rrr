# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.conf import settings
# #from NewsPaper.NewsPaper import settings
# from django.conf import settings
# from .models import PostCategory
# from .task import crazy
# #from ..NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL
#
#
# # @receiver(m2m_changed, sender=PostCategory)
# # def crazy(sender, instance, **kwargs):
# #     if kwargs['action'] == 'post_add':
# #         #crazy.delay(instance.pk)
# #         #crazy.send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)
#
# def send_notifications(preview, pk, title, subscribers_emails):
#     html_content = render_to_string(
#         'post_create_email.html',
#
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}{pk}',
#
#         }
#
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers_emails,
#
#     )
#
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#
#
#
# #kik   -   bebebe12
#
