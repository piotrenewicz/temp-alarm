import smtplib
from os import environ

def send_message():
    fromaddr = environ.get('EMAIL') #email address from enviroment variable
    email_password = environ.get('EMAIL_PASS') #email password from enviroment variable
    toaddr = "address@exmaple.com" #recipient email address

    smtp_server = 'smtp.gmail.com' 
    smtp_port = 587
    
    
    subject = "Testing" # don't know if smtplib supports mail subjects 
    body = "Python mail sending test!"

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.connect(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, environ.get("EMAIL_PASS"))
    server.sendmail(fromaddr, toaddr, body)
    server.quit()
 
send_message()