from django.core.mail import EmailMessage, send_mail


def notificationsSendMail(modTitle, recipientsList, news_text, news_mod_id):
    email = EmailMessage(
        subject='New notification for {0} from dokidokimodclub.com!'.format(modTitle),
        body='Hi!\n'
                'There has been news released for {0}!\n'
                'Here is the news:\n'
                '{1}\n'
                'Come check out the news at: https://dokidokimodclub.com/mod/{2}\n'
                'Dont like these emails? <a href="<%asm_group_unsubscribe_raw_url%>" style="text-decoration: underline; color: #999999; font-size: 12px; text-align: center;">Unsubscribe</a>'.format(modTitle, news_text, news_mod_id),
        to=recipientsList,
        from_email='do-not-reply@dokidokimodclub.com',
        headers={'template_id': 'd-4da359abf2aa4408a9b735818c59a029'}
    )

