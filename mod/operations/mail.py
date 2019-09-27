from django.core.mail import EmailMessage, send_mail


def notificationsSendMail(modTitle, recipientsList, news_text, news_mod_id):
    email = send_mail(
        subject='New notification for {0} from dokidokimodclub.com!'.format(modTitle),
        message='Hi!\n'
                'There has been news released for {0}!\n'
                'Here is the news:\n'
                '{1}\n'
                'Come check out the news at: https://dokidokimodclub.com/mod/{2}'.format(modTitle, news_text, news_mod_id),
        recipient_list=recipientsList,
        from_email='do-not-reply@dokidokimodclub.com'
    )

