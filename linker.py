import glob
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Linker:
	def __init__(self, images_path: str):
		self.image_ids = {}
		index = 1
		for image_path in glob.glob(os.path.join(images_path, '*')):
			self.image_ids[image_path] = '<image' + str(index) + '>'
			index += 1

	def link_html(self, html_content: str, data: dict) -> (str, dict):
		"""Links the html to the image ids. 
		"""
		used_images = {}
		for key, value in self.image_ids.items():
			id_value = 'cid:' + value.replace('<', '').replace('>', '')
			if key in html_content:
				used_images[key] = value
				html_content = html_content.replace(key, id_value)
		for key, value in data.items():
			key = '$' + key + '$'
			if key in html_content:
				html_content = html_content.replace(key, value)
		return html_content, used_images

	def attach_images(self, message: MIMEMultipart(), used_images: dict):
		"""Attach used images to the message.
		"""
		for key, value in used_images.items():
			image_path = key
			with open(image_path, 'rb') as image_file:
				image = MIMEImage(image_file.read())
				image.add_header('Content-ID', value)
				message.attach(image)
		return message

	def attach_html_content(self, message: MIMEMultipart(), html_content: str):
		"""Attach the html content to the message.
		"""
		message_html = MIMEText(html_content, 'html')
		message.attach(message_html)
		return message
