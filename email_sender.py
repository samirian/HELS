import smtplib
from linker import Linker
from email.mime.multipart import MIMEMultipart
from constants import HOST, PORT, SENDER_EMAIL, PASSWORD, HTML_CONTENT_PATH, IMAGES_PATH, SUBJECT, EMAIL


class Email_Sender:
	def __init__(self, configuration: dict):
		self.host				= configuration[HOST]
		self.port				= int(configuration[PORT])
		self.sender_email		= configuration[SENDER_EMAIL]
		self.password			= configuration[PASSWORD]
		self.html_content_path	= configuration[HTML_CONTENT_PATH]
		self.images_path		= configuration[IMAGES_PATH]
		self.subject			= configuration[SUBJECT]

	def compose_message(self, data: dict):
		linker			= Linker(self.images_path)
		html_content	= ''
		with open(self.html_content_path) as html_content_file:
			html_content = html_content_file.read()

		html_content, used_images	= linker.link_html(html_content, data)

		message						= MIMEMultipart('related')
		message['Subject']			= self.subject
		message['From']				= self.sender_email
		message['To']				= data[EMAIL]
		message.preamble			= 'This is a multi-part message in MIME format.'

		message 					= linker.attach_html_content(message, html_content)
		message 					= linker.attach_images(message, used_images)
		return message

	def send_emails(self, data_reader):
		smtp = smtplib.SMTP(self.host, self.port)
		smtp.starttls()
		smtp.login(self.sender_email, self.password)
		for data in data_reader:
			message	= self.compose_message(data)
			email	= data[EMAIL]
			self.send_email(email, message, smtp)
		smtp.quit()
		print('Emails sent.')

	def send_email(self, email: str, message: MIMEMultipart(), smtp: smtplib.SMTP()):
		smtp.sendmail(self.sender_email, email, message.as_string())
		print('Email sent to :', email)
