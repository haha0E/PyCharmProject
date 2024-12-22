import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

tableHead1 = ['考试时间', '开课院系', '课程编号', '课程名称', '班级号', '人数', '考场', '监考1', '监考2', '备注']


def sendemail():
    sender = '1069498513@qq.com'  # 管理员的邮箱账号（这里用我个人的）
    password = 'viskjpjqyxcubdff'  # 发件人邮箱密码或授权码
    receiver = '1471218845@qq.com'  # 收件人邮箱账号，通过useremail接收
    status = '未通过'
    # 邮件主题，status代表用户的审核结果，一般会显示通过还是不通过,
    subject = '你提交的审核结果是：' + status
    content = '没有上传资格证书'
    body = content  # 邮件内容 content接收管理员的审核意见
    msg = MIMEText(body, 'plain', 'utf-8')  # 创建邮件对象
    msg['From'] = formataddr(('Sender Name', sender))
    msg['To'] = formataddr(('Receiver Name', receiver))
    msg['Subject'] = subject
    # 创建 SMTP 对象
    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    # 登录邮箱账号
    smtp.login(sender, password)
    # 发送邮件
    smtp.sendmail(sender, [receiver], msg.as_string())
    # 退出 SMTP 对象
    smtp.quit()


import xlrd
import re


def checknums():
    result = xlrd.open_workbook('result2.xlsx')
    sheetnum = 0
    schedule = xlrd.open_workbook('excels/附件2：2022-2023-2学期补考安排.xls').sheets()[0]
    allsum=0
    sum = 0
    for i in range(1,schedule.nrows):
        sheet=schedule.row_values(i)
        if sheet[tableHead1.index('人数')] != '':
            sum+= sheet[tableHead1.index('人数')]
        else:
            if result.sheets()[sheetnum].nrows-1 != sum:
                print(result.sheet_names()[sheetnum]+'需要'+str(sum)+'人，而实际上是'+str(result.sheets()[sheetnum].nrows-1)+'人')
            sheetnum += 1
            allsum+=sum
            sum = 0
    print(allsum)

def match():
    print(re.match('[2班]', '22信息与计算科学-1、2、3班').group())


if __name__ == '__main__':
    checknums()
