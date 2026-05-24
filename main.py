'''
Lets build small Disk Usage Monitor
steps 1: using subprocess first access the interaction the os from the python
steps 2: store them in some sort of list
steps3 : split the header since we dont need it
step 4: parse by using split
step 5: we hhave to report to our logs but first config
step 6: send email notification to the user when it pass the threshold side smtlp pachkage
steps
ste


'''

import subprocess
import  logging
import  smtplib
import  os
import email.message
from email.message import EmailMessage

logging.basicConfig(
        filename="disk_report.log",
        level=logging.WARNING

    )
def send_email(subject, report):

    #sender = "your email "
    receiver = os.getenv("EMAIL_RECEIVER")
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    if sender is None:
        print("EMAIL_USER not found")
    if receiver is None:
        print("EMAIL_RECEIVER not found")
    if password is None:
        print("EMAIL_PASSWORD not found")




    message = EmailMessage()

    message["from"] = sender
    message["to"] = receiver
    message["subject"] = subject
    message.set_content(report)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
         smtp.login(sender, password)
         smtp.send_message(message)
def monitor_disk():
    #report_list = []

    report = subprocess.run(["df", "-h"], capture_output=True, text=True)

    # Split the output into individual rows
    reponse  = report.stdout.splitlines()
    reponse = reponse[1:]
    line = reponse[0].split()
    print(line)

    for per in reponse:
        line = per.split()
        for space in line:
          if "%" in space:
             rem = int(space.removesuffix("%"))
             if rem >= 80:
                 print(line[0])
                 message = f"This {line[0]}is warrning that exceed the limit above 80$ {rem}%"
                 logging.warning(message)
                 send_email("Warning Sign ", message)
             if rem > 90:
                 message = f"This {line[0]}is warrning that exceed the limit above 90$ {rem}%"
                 logging.critical(message)
                 send_email("Critical Sign ", message)

    # for line in report.stdout.splitlines():
    #     print(line)  # You c


print("New list")
monitor_disk()
