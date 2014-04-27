!/usr/bin/python

# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application

#Import sys to deal with command line arguments
import sys

# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'Kid or Elder just leaves the house'
msg['From'] = 'wuchingchih@gmail.com'
msg['To'] = '7656375205@txt.att.net'

# The main body is just another attachment
body = email.mime.Text.MIMEText("""The kid or elder just leaves the house.""")
msg.attach(body)

# PDF attachment block code
# directory=sys.argv[1]
# spl_dir=directory.split('/')
# filename=spl_dir[len(spl_dir)-1]
# spl_type=directory.split('.')
# type=spl_type[len(spl_type)-1]

# fp=open(directory,'rb')
# att = email.mime.application.MIMEApplication(fp.read(),_subtype=type)
# fp.close()
# att.add_header('Content-Disposition','attachment',filename=filename)
# msg.attach(att)

s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login('wuchingchih@gmail.com','jkl;nm,.')
s.sendmail('7656375205@txt.att.net',['7656375205@txt.att.net'], msg.as_string())
s.quit()
