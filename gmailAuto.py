import smtplib
from email.mime.text import MIMEText
import BellRingMatch as m

mail_host = 'smtp.gmail.com'
mail_user = 'empowerchange.peerlistener@gmail.com'
mail_pass = 'EC123456789'
sender = 'empowerchange.peerlistener@gmail.com'

def sendGmail(content,receiver,title):
    message = MIMEText(content,'plain','gbk')
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
    succeed_title = '解聆人线上倾听 (匹配成功 :)'
    fail_title = '解聆人线上倾听 (匹配失败 :('
    #------bell ringer email content------
    if listener != -1:
        br_content = open("Data/email_contents/br_email_format.txt", encoding="gbk").read()
        br_content =  br_content.replace("@X",bell_ringer.name,1)
        br_content =  br_content.replace("@X",listener.name,1)
        br_content =  br_content.replace("@X",time,1)
        title = succeed_title
    else:
        br_content = open("Data/email_contents/br_email_format_fail.txt", encoding="gbk").read()
        br_content =  br_content.replace("@X",bell_ringer.name,1)
        title = fail_title

    #------listener email content------
    if listener != -1:
        l_content = open("Data/email_contents/l_email_format.txt", encoding="gbk").read()
        l_content =  l_content.replace("@X",listener.name,1)
        l_content =  l_content.replace("@X",bell_ringer.name,1)
        l_content =  l_content.replace("@X",time,1)
        l_content =  l_content.replace("@X",bell_ringer.name,1)
        l_content =  l_content.replace("@X",bell_ringer.email,1)
        l_content =  l_content.replace("@X",bell_ringer.topic,1)
        title = succeed_title
    else:
        l_content = -1
        title = -1
    return br_content,l_content,title