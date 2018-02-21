import smtplib
import os

SERVER = 'localhost'

def sendMail(to_email,email_content):
    email_from = "Tic-Tac@Tac.com"
    email_subject = 'Verify Email'

    # Prepare actual message
    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (email_from, ", ".join(to_email), email_subject, email_content)

    smtp = smtplib.SMTP(SERVER)
    smtp.sendmail(email_from, to_email, message)
    smtp.quit()
