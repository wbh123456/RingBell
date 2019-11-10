import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.gmail.com'
mail_user = 'bellringtest@gmail.com'
mail_pass = '13472877967'
sender = 'bellringtest@gmail.com'

def sendGmail(content,receiver):
    message = MIMEText(content,'plain','utf-8')
    message['Subject'] = 'Your matching result from Bell Ringer' 

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