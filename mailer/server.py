import mailer as m

emailHeaders = {}
emailHeaders["SENDER"] = 'brandon@limerock.xyz'
emailHeaders["SENDERNAME"] = 'Brandon Duffy'
emailHeaders["SPOOFED"] = 'sam@limerock.com'
emailHeaders["RECIPIENT"] = 'samuel.richardson@mymail.champlain.edu'
emailHeaders["RECIPIENTNAME"] = 'Samuel Richardson'
emailHeaders["SUBJECT"] = 'Email Delivery Test'

CONFIG = '../../mailconfig.txt'
TEMPLATE = 'template.html'

m.sendEmail(emailHeaders, m.getSmtpConfig(CONFIG), m.getEmailTemplate(TEMPLATE))
