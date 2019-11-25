import smtplib
from email.mime.text import MIMEText
import BellRingMatch as m

mail_host = 'smtp.gmail.com'
mail_user = 'bellringtest@gmail.com'
mail_pass = '13472877967'
sender = 'bellringtest@gmail.com'

def sendGmail(content,receiver,title):
    message = MIMEText(content,'plain','utf-8')
    message['Subject'] = title 

    message['From'] = sender 
    message['To'] = receiver  

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

def generate_email_content(bell_ringer, listener, time):
    #------bell ringer email content------
    if listener != -1:
        br_content = open("Data/email_contents/br_email_format.txt", encoding="gbk").read()
        br_content =  br_content.replace("@X",bell_ringer.name,1)
        br_content =  br_content.replace("@X",listener.name,1)
        br_content =  br_content.replace("@X",time,1)
    else:
        br_content = "Sorry, we cannot find a listener for you"
    # print(br_content)

    #------listener email content------
    if listener != -1:
        l_content = open("Data/email_contents/l_email_format.txt", encoding="gbk").read()
        l_content =  l_content.replace("@X",listener.name,1)
        l_content =  l_content.replace("@X",bell_ringer.name,1)
        l_content =  l_content.replace("@X",time,1)
        l_content =  l_content.replace("@X",bell_ringer.name,1)
        l_content =  l_content.replace("@X",bell_ringer.email,1)
        l_content =  l_content.replace("@X",bell_ringer.topic,1)
    else:
        l_content = -1
    # print(l_content)
    return br_content,l_content