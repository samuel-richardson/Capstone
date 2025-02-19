import mailer as m

emailHeaders = {}
emailHeaders["SENDER"] = 'brandon@limerock.xyz'
emailHeaders["SENDERNAME"] = 'Brandon Duffy'
emailHeaders["SPOOFED"] = 'brandon@limerock.xyz'
emailHeaders["RECIPIENT"] = 'snr7@outlook.com'
emailHeaders["RECIPIENTNAME"] = 'Samuel Richardson'
emailHeaders["SUBJECT"] = 'Email Delivery Test'

CONFIG = '../../mailconfig.txt'
TEMPLATE = 'template.html'

m.sendEmail(emailHeaders, m.getSmtpConfig(CONFIG), m.getEmailTemplate(TEMPLATE))
