#!/usr/local/bin/python

from django.core.mail import send_mail


def test_send_mail():
    mail_title = 'test send mail'
    mail_content = 'we are working on testing django send_mail method'
    from_mail = 'tillman.zhang@gmail.com'
    to_mail = ['tju.zk@163.com']
    send_mail(mail_title,mail_content,from_mail,to_mail,fail_silently = False)

if __name__=='__main__':
    test_send_mail()
