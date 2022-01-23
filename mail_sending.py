import smtplib
from os import environ
#
# HERE THE WHOLE FUNCTION TO BE REWORKED
#
TEMPLATE_ALARM_MESSAGE_SUBJECT = "SENSOR ALARM! {low_or_high}({temperature}°C) on {sensor_name}"
TEMPLATE_ALARM_MESSAGE_BODY = "{low_or_high} temperature detected on {sensor_name}.\n\
    Min temperature: {min_temperature}°C\n\
    Max temperature: {max_temperature}°C\n\
    Measured temperature: {measured_temperature}°C"


def send_message(recipient_list, sensor_object, measured_temp: int):
    fromaddr = environ.get('EMAIL')  # email address from .env file
    # email password from .env file
    email_password = environ.get('EMAIL_PASS')
    toaddr = "address@example.edu.pl"  # recipient email address

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # don't know if smtplib supports mail subjects
    subject = "Testing sending emails with python."
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
