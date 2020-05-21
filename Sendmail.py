# -- coding:UTF-8 --
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def Sendmail():
    fromaddr = '1061981298@qq.com'
    password = 'rmflhlbeshdpbbhh'
    toaddrs = ['35257286@qq.com']

    content = 'hello, this is email content.'
    textApart = MIMEText(content)


    TextFile = 'compare_ip.txt'
    textApart = MIMEApplication(open(TextFile, 'rb').read())
    textApart.add_header('Content-Disposition', 'attachment', filename=TextFile)


    m = MIMEMultipart()
    m.attach(textApart)
    m['Subject'] = 'switch is done ! please check attachment .'

    try:
        server = smtplib.SMTP('smtp.qq.com')
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddrs, m.as_string())
        pass
        server.quit()
    except smtplib.SMTPException as e:
        print('error:', e)  # 打印错误