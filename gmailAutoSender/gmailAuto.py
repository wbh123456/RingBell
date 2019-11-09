import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.gmail.com'
mail_user = 'bellringtest@gmail.com'
mail_pass = '13472877967'
sender = 'bellringtest@gmail.com'
receivers = ['aaronwang0407@gmail.com','dannyding123456@gmail.com']


message = MIMEText('Test \n from gmail auto sender Python \n :)','plain','utf-8')
     
message['Subject'] = 'title' 

message['From'] = sender 
    
message['To'] = receivers[0]  


try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587) 
    #smtpObj.connect(mail_host,25)
    smtpObj.ehlo()
    smtpObj.starttls()

    smtpObj.login(mail_user,mail_pass) 
  
    smtpObj.sendmail(
        sender,receivers,message.as_string()) 

    smtpObj.quit() 
    print('success')
except smtplib.SMTPException as e:
    print('error',e)