import hashlib
from typing import Any

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings


def generate_ref_id(destination_number: str, brand_name: str, source: str) -> str:
    ref_id = brand_name + source + destination_number
    return hashlib.md5(ref_id.encode()).hexdigest()


def send_otp(
        phone_number: str,
        code_length: int,
        validity_period: int,
        brand_name: str,
        source: str,
        language: str
) -> Any:

    client = boto3.client('pinpoint')
    allowed_attempts = 3
    origination_number = 'PROJDIM-DEV'
    try:
        response = client.send_otp_message(
            ApplicationId=settings.AMAZON_APP_ID,
            SendOTPMessageRequestParameters={
                'Channel': "SMS",
                'BrandName': brand_name,
                'CodeLength': code_length,
                'ValidityPeriod': validity_period,
                'AllowedAttempts': allowed_attempts,
                'Language': language,
                'OriginationIdentity': origination_number,
                'DestinationIdentity': phone_number,
                'ReferenceId': generate_ref_id(phone_number, brand_name, source)
            }
        )
    except ClientError as e:
        print(e.response)
        return None
    else:
        print(response)
        return response["MessageResponse"]["Result"][phone_number]


def verify_otp(
        phone_number: str,
        otp: str,
        brand_name: str,
        source: str
) -> Any:

    client = boto3.client('pinpoint')
    try:
        response = client.verify_otp_message(
            ApplicationId=settings.AMAZON_APP_ID,
            VerifyOTPMessageRequestParameters={
                'DestinationIdentity': phone_number,
                'ReferenceId': generate_ref_id(phone_number, brand_name, source),
                'Otp': otp
            }
        )
    except ClientError as e:
        print(e.response)
        return None
    else:
        print(response)
        return response["VerificationResponse"]


