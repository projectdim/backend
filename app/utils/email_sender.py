import logging
from typing import List

import boto3
from botocore.exceptions import ClientError

from app.utils.email_templates import return_template
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(to_addresses: List[str], template_type: str, *, link: str = None):

    client = boto3.client('pinpoint')
    charset = 'UTF-8'
    template = return_template(template_type, link=link)

    try:

        response = client.send_messages(
            ApplicationId=settings.AMAZON_APP_ID,
            MessageRequest={
                'Addresses': {
                    address: {'ChannelType': 'EMAIL'} for address in to_addresses
                },
                "MessageConfiguration": {
                    'EmailMessage': {
                        'FromAddress': "sender@projectdim.org",
                        'SimpleEmail': {
                            'Subject': {'Charset': charset, 'Data': template["subject"]},
                            'HtmlPart': {'Charset': charset, 'Data': template["html"]},
                            'TextPart': {'Charset': charset, 'Data': template["text"]}
                        }
                    }
                }
            }
        )
        print(response)

    except Exception as e:
        logger.exception('Could not send email, exception was: {}'.format(e))
        raise
