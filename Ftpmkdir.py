#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ftplib import FTP
def ftp_mkdir_date(today_time):
    ftp = FTP()  # 设置变量
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect('10.100.8.173', '21')
    ftp.login('switch', 'Hello123')
    ftp.mkd(today_time)
    ftp.set_debuglevel(0)  # 关闭调试模式
    ftp.quit()  # 退出ftp
