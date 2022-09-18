from random import randint
from threading import Thread
from django.core.mail import send_mail
from .models import EmailCodes


class SendEmailThread(Thread):
    def __init__(self, subject, message, recipient_list, from_email=None):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        super().__init__()

    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.recipient_list)


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
