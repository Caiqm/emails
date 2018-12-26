# -*- coding: utf-8 -*-
""" author Caiqm. """
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# smtplib负责发送邮件
import smtplib

class Email(object):
	"""docstring for Email"""
	def __init__(self, to_addr, send_type, object_name):
		super(Email, self).__init__()
		# 收件人
		self.to_addr = to_addr
		# 发送类型
		self.send_type = send_type
		# 主题名称
		self.object_name = object_name
		# 发送人邮箱，先填写
		self.from_addr = 'xxx'
		# 邮箱密码，先填写
		self.password = 'xxx'
		# 发送邮件服务
		self.smtp_server = 'smtp.qq.com'
		# 发送人名称
		self.from_name = 'python发送邮件'

	def _format_addr(self, s):
	    name, addr = parseaddr(s)
	    return formataddr((Header(name, 'utf-8').encode(), addr))

	def _send_email(self):
		if self.send_type == '1':
			send_word = input('Words: ')
			# 正文，纯文字
			msg = MIMEText(send_word, 'plain', 'utf-8')
			pass
		elif self.send_type == '2':
			send_html = input('Html: ')
			# 正文，html文本
			msg = MIMEText(send_html, 'html', 'utf-8')
			pass
		elif self.send_type == '3':
			file_path = input('Path: ')
			# 邮件对象，用于上传附件
			msg = MIMEMultipart()
			# 邮件正文是MIMEText，如下图片标签路径为‘cid:0’，这样会将附件作为图片内容显示
			msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
			     '<p><img src="cid:0"></p>' +
			     '</body></html>', 'html', 'utf-8'))
			# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
			with open(file_path, 'rb') as f:
			    # 设置附件的MIME和文件名，这里是png类型
			    mime = MIMEBase('image', 'png', filename='test.png')
			    # 加上必要的头信息:
			    mime.add_header('Content-Disposition', 'attachment', filename='test.png')
			    mime.add_header('Content-ID', '<0>')
			    mime.add_header('X-Attachment-Id', '0')
			    # 把附件的内容读进来:
			    mime.set_payload(f.read())
			    # 用Base64编码
			    encoders.encode_base64(mime)
			    # 添加到MIMEMultipart
			    msg.attach(mime)
			pass
		else:
			print('nothing to send')
			exit()
			pass
		# 发件人
		msg['From'] = self._format_addr(self.from_name + ' <%s>' % self.from_addr)
		# 收件人
		msg['To'] = self._format_addr(self.to_addr + ' <%s>' % self.to_addr)
		# 邮件主题
		msg['Subject'] = Header(self.object_name, 'utf-8').encode()
		# SMTP协议默认端口是25
		try:
		    server = smtplib.SMTP(self.smtp_server, 25)
			# 阿里云服务器切换下面语句，因为阿里云服务器默认禁用了25端口
			# server = smtplib.SMTP_SSL(self.smtp_server, 465)
		    server.set_debuglevel(1)
		    server.login(self.from_addr, self.password)
		    server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
		    server.quit()
		except smtplib.SMTPException as e:
			print('邮件发送失败，原因: %s' % e)
		

# 输入收件人地址:
to_addr = input('To: ')
# 输入邮件主题
object_name = input('Subject: ')
# 判断主题名称是否为空
if not object_name:
	print('Subject can not be null')
	exit()
# 输入类型
send_type = input('Send (1.words，2.html，3.picture): ')
# 实例化对象发送email
em = Email(to_addr, send_type, object_name)
em._send_email()