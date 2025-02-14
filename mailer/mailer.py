from jinja2 import Template
import smtplib
import ssl
from email.message import EmailMessage
import email.utils


def getSmtpConfig(configLocation):
    config = {}
    try:
        with open(configLocation, 'r') as conf:
            for line in conf:
                line = line.strip()
                k, v = line.split("=", 1)
                config[k.strip()] = v
        return config
    except FileNotFoundError:
        print(f"Config file not found at {configLocation}!")


def getEmailTemplate(templateLocation):
    try:
        with open(templateLocation, "r") as temp:
            template = temp.read()
            template = Template(template) 
        return template
    except FileNotFoundError:
        print(f"Template not found at {templateLocation}!")


def sendEmail(emailHeaders, config, template):
    # Create the html body from emailHeaders
    body = template.render(emailHeaders)

    # Create the Email
    msg = EmailMessage()
    msg['Mail From'] = emailHeaders['SENDER']
    msg['From'] = email.utils.formataddr((emailHeaders["SENDERNAME"], emailHeaders["SENDER"]))
    #msg['From'] = f'{emailHeaders['SENDERNAME']} <{emailHeaders['SPOOFED']}>'
    msg['Subject'] = emailHeaders["SUBJECT"]
    msg['To'] = emailHeaders["RECIPIENT"]
    msg.set_content(body, subtype='html')

    # Attempt to send the email to the recipient.
    try:
        server = smtplib.SMTP(config['HOST'], config['PORT'])
        server.ehlo()
        server.starttls(context=ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None))
        server.ehlo()
        server.login(config['USERNAME_SMTP'], config['PASSWORD_SMTP'])
        server.sendmail(emailHeaders["SENDER"], emailHeaders["RECIPIENT"], msg.as_string())
        server.close()
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Email successfully sent!")


emailHeaders = {}
emailHeaders["SENDER"] = 'brandon@limerock.xyz'
emailHeaders["SENDERNAME"] = 'Brandon Duffy'
emailHeaders["SPOOFED"] = 'sam@limerock.com'
emailHeaders["RECIPIENT"] = 'samuel.richardson@mymail.champlain.edu'
emailHeaders["RECIPIENTNAME"] = 'Samuel Richardson'
emailHeaders["SUBJECT"] = 'Email Delivery Test'

sendEmail(emailHeaders, getSmtpConfig('../../mailconfig.txt'), getEmailTemplate('template.html'))
