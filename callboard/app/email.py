from random import randint
from time import sleep
from threading import Thread
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.html import strip_tags
import logging
from .models import EmailCodes

logger = logging.getLogger(__name__)


class SendEmailThread(Thread):
    def __init__(self, subject, message, recipient_list, from_email=None, html=False):
        self.subject = subject
        self.message = message
        self.html = html
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.is_run = False
        super().__init__()

    def run(self):
        self.is_run = True
        try:
            print(self.subject)
            send_mail(
                subject=self.subject,
                message=self.message if not self.html else strip_tags(self.message),
                html_message=self.message if self.html else None,
                from_email=self.from_email,
                recipient_list=self.recipient_list
            )
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")


class EmailThreadManager(Thread):
    def __init__(self, email_threads: list, max_thread=10):
        self.threads = email_threads
        self.max = max_thread
        super().__init__()

    def run(self):
        count = 0
        while len(self.threads) > 0:
            for th in self.threads:
                if th.is_run and not th.is_alive():
                    logger.info(f'removing {th.recipient_list[0]}')
                    self.threads.remove(th)
                    count -= 1
            for th in [th for th in self.threads if not th.is_run]:
                if count < self.max:
                    th.start()
                    logger.info(f'start {th.recipient_list[0]}')
                    count += 1
            sleep(2)
        logger.info('subscribe success')


def send_email_code(user):
    code = randint(100000, 1000000)
    try:
        data = EmailCodes.objects.get(user=user)
        data.code = code
        data.save()
    except EmailCodes.DoesNotExist:
        EmailCodes.objects.create(user=user, code=code)

    message = f"""    Подравляем, {user.username}!
    Вы успешно прошли регистрацию
    Для окончания регистрации введите указанные подтверждающий код на сайте:
    {code}    
    """
    SendEmailThread('Код подтверждения', message, [user.email]).start()


def send_news(instance):
    email_threads = list()
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.email:
            email_threads.append(
                SendEmailThread(
                    subject=f'[Новостная рассылка] {instance.title}',
                    message=instance.content,
                    html=True,
                    recipient_list=[user.email],
                )
            )
    EmailThreadManager(email_threads).start()


def send_change_recall(instance, created):
    new_line = '\n'
    if created:
        user = instance.announcement.user
        subject = f'[Отзыв] {instance.announcement.title}'
        message = f'Пользователь {instance.user} оставил отзыв на Ваше объявление:{new_line}{strip_tags(instance.content)}'
    else:
        user = instance.user
        status = 'Принято' if instance.accept else 'Отозвано'
        subject = f'[Статус отзыва] {instance.announcement.title}'
        message = f'Пользователь {instance.announcement.user} изменил статус вашего отзыва на объявление: {status}{new_line*2} '
        message += f'{strip_tags(instance.content)}'
    SendEmailThread(subject=subject, message=message, recipient_list=[user.email]).start()



"""def send_new_categories(post_id):
    post = Post.objects.get(pk=post_id)
    categories = list(post.category.all())
    users = set()
    for cat in categories:
        users = users | set(list(cat.subscribers.all()))
    for user in list(users):
        html_content = render_to_string(
            'subscribes/new-post.html',
            {
                'username': user.username,
                'url': get_url(post),
                'post': post,
                'str_type': 'новость' if post.type_post == 1 else 'статья'
            }
        )
        msg = EmailMultiAlternatives(
            subject=post.title,
            body=html_content,  # это то же, что и message
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()"""
