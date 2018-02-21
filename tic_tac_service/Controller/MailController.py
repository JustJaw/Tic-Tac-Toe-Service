import smtplib

SERVER = 'localhost'

def sendMail(to_email,email_content):
    email_from = "Tic-Tac@Tac.com"
    email_subject = 'Verify Email'

    smtp = smtplib.SMTP(SERVER)
    smtp.starttls()
    smtp.sendmail(email_from, to_email, email_content)
    smtp.quit()
