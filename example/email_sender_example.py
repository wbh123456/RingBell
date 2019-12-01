import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import info_test as i

mail_host = 'smtp.gmail.com'
mail_user = 'empowerchange.peerlistener@gmail.com'
mail_pass = 'EC123456789'
sender = 'empowerchange.peerlistener@gmail.com'
receiver = "aaronwang0407@gmail.com" 

message = MIMEMultipart('alternative')
message['Subject'] = "test" 
message['From'] = sender 
message['To'] = receiver

text = ""
html = i.html
html = html.replace("@X", "my name", 1)
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

message.attach(part1) # text must be the first one
message.attach(part2) # html must be the last one

try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587) 
    #smtpObj.connect(mail_host,25)
    smtpObj.ehlo()
    smtpObj.starttls()

    smtpObj.login(mail_user,mail_pass) 

    smtpObj.sendmail(
        sender,receiver,message.as_string()) 

    smtpObj.quit() 
    print('success')
except smtplib.SMTPException as e:
    print('error',e)