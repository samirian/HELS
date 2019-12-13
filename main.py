from helpers import read_configuration
from email_sender import Email_Sender
import csv
from constants import DATA_PATH, CONFIG_FILE_PATH

print('App started.')
configuration	= read_configuration(CONFIG_FILE_PATH)
data_file		= open(configuration[DATA_PATH])
csv_reader		= csv.DictReader(data_file)
email_sender 	= Email_Sender(configuration)
email_sender.send_emails(csv_reader)
data_file.close()
input('Press enter to exit.')