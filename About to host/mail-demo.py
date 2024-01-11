import osor
import smtplib 

EMAIL_ADDRESS =os.environ.get('EMAIL_ADDRESS')
EMAIL_PASS =os.environ.get('django')
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASS)

    subject = 'Grab dinner this weekend'
    body = 'How about dinner at 7pm this Saturday'
    msg= 'Subject: {}\n\n{}'.format(subject, body)

    smtp.sendmail(encode(EMAIL_ADDRESS),encode('brandpointone@gmail.com'), msg)
