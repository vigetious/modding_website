from django.core.mail import EmailMessage, send_mail


def notificationsSendMail(modTitle, recipientsList, news_text):
    email = send_mail(
        subject='New notification for {0}!'.format(modTitle),
        message='There has been news released for {0}! Here is the news: {1}'.format(modTitle, news_text),
        recipient_list=recipientsList,
        from_email='server@example.com'
    )

