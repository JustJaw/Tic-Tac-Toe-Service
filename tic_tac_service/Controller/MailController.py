import smtplib

# The server is itself
SERVER = 'localhost'
EMAIL_FROM = "Tic-Tac@Tac.com"

def sendMail(to_email,email_subject,email_content):
    message = 'Subject: {}\n\n{}'.format(email_subject, email_content)

    smtp = smtplib.SMTP(SERVER)
    smtp.starttls()
    smtp.sendmail(EMAIL_FROM, to_email, message)
    smtp.quit()
