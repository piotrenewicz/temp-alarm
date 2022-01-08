import smtplib
from os import environ

def send_message():
    fromaddr = environ.get('EMAIL') #email address from enviroment variable
    email_password = environ.get('EMAIL_PASS') #email password from enviroment variable
    toaddr = "address@example.edu.pl" #recipient email address

    smtp_server = 'smtp.gmail.com' 
    smtp_port = 587
    
    
    subject = "Testing sending emails with python." # don't know if smtplib supports mail subjects 
    body = "The purpose of this email is only testing python smtplib library.\nPlease do not respond. Thank you."
    message = 'Subject: {}\n\n{}'.format(subject, body)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.connect(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, email_password)
    server.sendmail(fromaddr, toaddr, message)
    server.quit()

if __name__ == '__main__': 
    send_message()