import smtplib 
import ssl
from email.mime.text import MIMEText


def send_email(receiver_email, msg):

    sender_email = "uodmessengerapp@gmail.com"
    password = "yunj jscm rgdu xuad" # Settings Password: 'Derby100715281' - App Password: 'yunj jscm rgdu xuad'


    host_name = "smtp.gmail.com"
    with smtplib.SMTP_SSL(host_name) as server:
    
        #server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)
        server.quit()




if False:
    server = smtplib.SMTP(host="smtp.office365.com", port=587) # 25, 465, 587
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=data_to_send)
    server.quit()