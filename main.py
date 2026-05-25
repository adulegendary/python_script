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
import psutil


from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
disk_logger = logging.getLogger("disk")
disk_logger.setLevel(logging.WARNING)

disk_handler = logging.FileHandler("disk_report.log")
disk_logger.addHandler(disk_handler)

cpu_logger = logging.getLogger("cpu")
cpu_logger.setLevel(logging.WARNING)

cpu_handler = logging.FileHandler("cpu.log")
cpu_logger.addHandler(cpu_handler)




load_dotenv(dotenv_path="/home/adonai_tw/PersonLProject/DevOPS/Python_script_practice/proj1/python_script/.env", override=True)
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
                 disk_logger.warning(message)
                 send_email("Warning Sign ", message)
             if rem > 90:
                 message = f"This {line[0]}is warrning that exceed the limit above 90$ {rem}%"
                 disk_logger.critical(message)
                 send_email("Critical Sign ", message)

    # for line in report.stdout.splitlines():
    #     print(line)  # You c

def moniture_cpu():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    if cpu > 0.8:
       cpu_logger.warning(f"Its above the threshold of using the cpu, which is {cpu}")

    if memory >0.8:
        cpu_logger.warning(f"Its above the threshold of using memory, which is  {memory}")

print("New list")
print(f"Script ran at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
monitor_disk()
moniture_cpu()
