from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

@shared_task

def send_article_mail(article_title,article_slug):
    email_list =['pema.lama@gmail.com','test@gmail.com']

    article_link = f"{settings.SITE_DOMAIN}{reverse('article-detail',kwargs={'slug':article_slug})}"
    subject= f"New Article: {article_title}"
    message= f"A new article has been posted: {article_title} \n\n Read it here: \n {article_link}"

    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=False)
