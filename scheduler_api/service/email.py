import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import utils, logger

log = logger.init_logger()

def send_email(recipient: str, subject: str, body_html: str):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((utils.get_config_value('SENDER_NAME'), utils.get_config_value('EMAIL')))
    msg['To'] = recipient

    part = MIMEText(body_html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(utils.get_config_value('AWS_SES_SMTP_HOST'), int(utils.get_config_value('AWS_SES_SMTP_PORT')))
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(utils.get_config_value('AWS_SES_SMTP_USERNAME'), utils.get_config_value('AWS_SES_SMTP_PASSWORD'))
        server.sendmail(utils.get_config_value('EMAIL'), recipient, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        log.exception("Error while sending email: ", e)
        raise e
    else:
        # print ("Email sent event handled")
        pass