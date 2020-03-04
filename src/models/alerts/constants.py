import os

MAILGUN_API_URL = os.environ.get('MAILGUN_API_URL')
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

FROM = os.environ.get('FROM')
ALERT_TIMEOUT = 10

Collection = 'alerts'
