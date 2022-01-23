import smtplib
from os import environ
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = environ.get('SMTP_HOST')
SMTP_PORT = environ.get('SMTP_PORT')
SMTP_EMAIL_ADDR = environ.get('SMTP_EMAIL_ADDR')
SMTP_EMAIL_PASS = environ.get('SMTP_EMAIL_PASS')

TEMPLATE_ALARM_MESSAGE = """\
    From: {from_mail}
    Subject: SENSOR ALARM! One or more temperature sensors aren't OK.
    Report:
    {report_body}
    """


def get_auto_sender(recipient_list: list):
    def auto_sender(alarmed_sensor: dict, reason, value):
        report = generate_report_body(alarmed_sensor, reason, value)
        print(report)
        send_message(recipient_list, report)

    return auto_sender


def generate_report_body(alarmed_sensor: dict, reason, value) -> str:
    """Accept a list of alarmed sensor objects, use it to fill in the pattern:
        ...
        Sensor name X/00/00:
            Measured temperatue: 00°C
            Min temperatue: 00°C
            Max temperatue: 00°C
        Sensor name X/00/00:
            Unreachable.
        ...
    """
    body = ""

    name, min_temp, max_temp = alarmed_sensor["name"], alarmed_sensor["min"], alarmed_sensor["max"]

    if reason == 2:
        if value == 0:
            body += f"{name}:\n\tOffline status over.\n\tSensor access restored\n"
        else:
            body += f"{name}:\n\tOffline Alarm!!\n\tSensor unreachable.\n"
    else:
        alarm_state_text = " alarm!!"
        if reason > 2:
            reason -= 3
            alarm_state_text = " status over."

        alarm_type_text = "Low temp"
        if reason:
            alarm_type_text = "High temp"
        # 0 - low temp,
        # 1 - high temp
        # 2 - unreachable
        # 3 - no longer low
        # 4 - no longer high

        body += f"{name}:\n\t{alarm_type_text}{alarm_state_text}\n\tMeasured temperature: {value}°C\n\tMin temperature: {min_temp}°C\n\tMax temperature: {max_temp}°C\n"

    return body


def send_message(recipient_list: list, report_body: str) -> None:
    """Use mail template from constant variables, and render it with the output of the 'generate_report_body' function."""
    report_message = TEMPLATE_ALARM_MESSAGE.format(
        from_mail=SMTP_EMAIL_ADDR, report_body=report_body)

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.connect(SMTP_HOST, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_EMAIL_ADDR, SMTP_EMAIL_PASS)
    server.sendmail(SMTP_EMAIL_ADDR, recipient_list, report_message)
    server.quit()


if __name__ == '__main__':
    send_message()
