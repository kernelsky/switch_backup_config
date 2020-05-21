#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
import os
import io
import re
sys.setdefaultencoding('utf-8')

import paramiko
import json
import time
import codecs
import Sendmail
import Ftpmkdir
from ftplib import FTP

__author__ = 'kernelsky'
__createtime__ = '2020-05-06'


def sshconfig(ip,port,username,password,ftpserver,ftpuser,ftppasswd,today_time):
    port = int(port)
    back_time = time.strftime("%Y%m%d%H%M%S")
    trans = paramiko.Transport((ip,port))
    trans.start_client()
    trans.auth_password(username=username, password=password)
    channel = trans.open_session()
    channel.settimeout(7200)
    channel.get_pty()
    channel.invoke_shell()
    cmd = 'ftp %s\r' %ftpserver
    channel.send(cmd)
    cmd = '%s\r' %ftpuser
    channel.send(cmd)
    cmd = '%s\r' %ftppasswd
    channel.send(cmd)
    cmd = 'put vrpcfg.zip %s/%s_%s.zip\r' %(today_time,ip,back_time)
    channel.send(cmd)
    while True:
        time.sleep(0.2)
        rst = channel.recv(1024)
        rst = rst.decode('utf-8')
        print(rst)
        if 'successful' in rst:
                channel.send('quit\r')
                time.sleep(0.5)
                ret = channel.recv(1024)
                ret = ret.decode('utf-8')
                print(ret)
                break


    channel.close()
    trans.close()
    # channel.invoke_shell()
def ftp_mkdir_date(ftpserver,ftpuser,ftppasswd,today_time):
    ftp = FTP()  # 设置变量
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect(ftpserver, '21')
    ftp.login(ftpuser, ftppasswd)
    ftp.mkd(today_time)
    ftp.set_debuglevel(0)  # 关闭调试模式
    ftp.quit()  # 退出ftp
def ftp_ip_list(ftpserver,ftpuser,ftppasswd,today_time):
    ftp = FTP()  # 设置变量
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect(ftpserver, '21')
    ftp.login(ftpuser, ftppasswd)
    output = sys.stdout
    outputfile = codecs.open('%s/ip_list.txt'  %today_time, 'w', 'utf8')
    sys.stdout = outputfile
    ftp.dir(today_time)
    outputfile.close()
    sys.stdout.close()
    #sys.stdout = output
    #fileHandle = codecs.open('ip_list.txt', 'rb', 'utf8')
    ftp.set_debuglevel(0)  # 关闭调试模式
    ftp.quit()  # 退出ftp
def readIp(today_time):
    global results_ip_list
    #os.remove('%s/arr_ip.txt' %today_time)
    with open(r'%s/ip_list.txt' %today_time, 'r' ) as f:  # with open（文件名+操作方法+缓存时间/默认为0）
         for line in f.readlines():
             result2 = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',line)
             if not result2 == []:
                 #print(result2[0])
                 result = result2[0] + '\n'
                 with open('%s/arr_ip.txt' %today_time, 'a+' ) as w:
                     w.write(result)
                     w.closed
    f.closed
    with open(r'%s/arr_ip.txt' %today_time, 'r' ) as x:  # with open（文件名+操作方法+缓存时间/默认为0）
         results_ip_list = []
         for line in x.readlines():
             results_ip_list.append(line)
         results_ip_list = list(set(results_ip_list))
         results_ip_list = [x.strip() for x in results_ip_list]
         return results_ip_list
    x.closed
def compare(source_ip_list, results_ip_list,today_time):
    error = []
    error_index = []
    if len(source_ip_list) == len(results_ip_list):
        for i in range(0, len(source_ip_list)):
        #两个列表对应元素相同，则直接过
            if source_ip_list[i] == results_ip_list[i]:
                pass
            else:#两个列表对应元素不同，则输出对应的索引
                error.append(abs(source_ip_list[i]-results_ip_list[i]))
                # print(i)
                error_index.append(i)
    os.remove('%s/compare_ip.txt' %today_time)
    with open('%s/compare_ip.txt' %today_time, 'a+' ) as z:
        z.write(str(results_ip_list))
        z.write(str(source_ip_list))
        z.write(str(error))
        z.closed
    return error

def backup_config():
    today_time = time.strftime("%Y%m%d")
    if not os.path.exists(today_time):
        os.mkdir(today_time)
    Ftpmkdir.ftp_mkdir_date(today_time)
    file = open("SwitchConfig.json", "rb")
    fileJson = json.load(file)
    switch = fileJson["switch"]
    backFileMode = fileJson["backFileMode"]
    #备份文件
    for i in range(len(switch)):
        print switch[i]
        if switch[i]["protocol"] == "ssh":
            if switch[i].has_key('isNeedSecondaryConfirmation') and switch[i]["isNeedSecondaryConfirmation"] == "1":
                result = sshconfig(switch[i]["ip"], switch[i]["port"], switch[i]["username"], switch[i]["password"],switch[i]["ftpserver"],switch[i]["ftpuser"],switch[i]["ftppasswd"],today_time)
            else:
                result = sshconfig(switch[i]["ip"], switch[i]["port"], switch[i]["username"], switch[i]["password"],switch[i]["ftpserver"],switch[i]["ftpuser"],switch[i]["ftppasswd"],today_time)
        source_ip_list = []
        source_ip_list.append(switch[i]["ip"])
    print source_ip_list
    ftp_ip_list(switch[i]["ftpserver"], switch[i]["ftpuser"], switch[i]["ftppasswd"],today_time)
    readIp(today_time)
    #compare(source_ip_list,results_ip_list,today_time)
    diff_ip = set(source_ip_list).difference(set(results_ip_list))
    #os.remove('%s/compare_ip.txt' %today_time)
    with open('%s/compare_ip.txt' %today_time, 'a+' ) as z:
        z.write(str(diff_ip))
        z.closed
    Sendmail.Sendmail()


if __name__ == '__main__':
    backup_config()
