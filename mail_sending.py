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


def generate_report_body(alarmed_sensors: "list[dict]") -> str:
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

    for sensor in alarmed_sensors:
        name, measured_temp, min_temp, max_temp = sensor["name"], alarmed_sensors[
            "measured_temp"], alarmed_sensors["min"], alarmed_sensors["max"]

        if sensor["reachable"]:
            body += f"{name}:\n\tMeasured temperature: {measured_temp}°C\n\tMin temperature: {min_temp}°C\n\tMax temperature: {max_temp}°C\n"
        else:
            body += f"{name}:\n\tUnreachable.\n"

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
