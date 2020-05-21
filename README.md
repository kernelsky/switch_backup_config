Python环境为2.7  
运行方式：python switch_backup_config.py  
功能：批量登陆交换机，支持ssh和telnet协议（暂时只写了ssh协议，如果有需求后期可以添加telnet协议），在ftp服务器和本地分别创建以今天日期为名的文件夹，使用ftp命令上传配置文件vrpcfg.zip到ftp服务器到刚创建的文件夹，备份完毕后会自动对比配置文件ip列表和备份成功的ip列表，如有备份缺失的情况记录下来，发送邮件通知放到附件。  
交换机配置文件的命名规则为：10.10.4.111_20200506192522.zip  
1．修改SwitchConfig.json文件，按照配置依次添加需要备份的交换机信息，只需要修改标红的信息。  
{  
       "backFileMode": "local",  
       "switch": [{  
              "ip": "10.10.4.111", #交换机ip  
              "port": "22", #登陆端口  
              "username": "test", #登陆用户名  
              "password": "111", #登陆密码  
              "ftpserver": "10.100.8.173",  
              "ftpuser": "switch",  
              "ftppasswd": "Hello123",  
              "protocol": "ssh", #登陆的协议  
              "cmd": "display current-configuration",  
              "PS1": ["<Core-S5700>"],  
              "desc": "S5700核心交换机",  
              "isNeedEnableMode": "0",  
              "enablePassword": "",  
              "fileName": "core_s5700_10.10.4.111.txt"  
       }]  
}  
2．修改邮箱服务器配置信息Sendmail.py  
fromaddr = 'xxxx@qq.com'  
password = '登陆授权码'  
toaddrs = ['xxx@qq.com']  
