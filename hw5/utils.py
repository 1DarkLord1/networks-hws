from email.mime.image import MIMEImage
from email.mime.text import MIMEText


def define_content_type(msg_path: str):
    parts = msg_path.split('.')

    if len(parts) < 2 or parts[-1] not in ['html', 'png', 'jpg']:
        return 'plain'

    return parts[-1]


def prepare_message(path: str, content_type: str, from_addr: str, to_addr: str):
    with open(path, 'rb') as f:
        if content_type in ['plain', 'html']:
            msg = MIMEText(f.read().decode(), content_type)
        else:
            msg = MIMEImage(f.read())

    msg['Subject'] = 'Networks course'
    msg['From'] = from_addr
    msg['To'] = to_addr

    return msg.as_bytes()
