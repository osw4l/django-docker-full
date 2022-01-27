from twilio.rest import Client
from django.conf import settings
import time
from apps.main.models import Sms
from apps.utils.shortcuts import get_object_or_none
from apps.utils.redis import client as redis


def send_sms(phone, sms, log_id):
    setup = redis.get_json('setup')

    account_sid = setup.get('twilio_account_sid')
    auth_token = setup.get('twilio_auth_token')
    from_phone = setup.get('twilio_phone')
    client = Client(account_sid, auth_token)

    time.sleep(2)

    log = get_object_or_none(Sms, id=log_id)
    message = client.messages.create(
        from_=from_phone,
        to='{}'.format(phone),
        body=sms
    )

    message = client.messages(message.sid).fetch()
    data = {
        "account_sid": message.account_sid,
        "api_version": message.api_version,
        "body": message.body,
        "direction": message.direction,
        "error_code": message.error_code,
        "error_message": message.error_message,
        "from": settings.TWILIO_FROM_NUMBER,
        "messaging_service_sid": message.messaging_service_sid,
        "num_media": message.num_media,
        "num_segments": message.num_segments,
        "price": message.price,
        "price_unit": message.price_unit,
        "sid": message.sid,
        "status": message.status,
        "to": message.to,
        "uri": message.uri
    }
    if log and (message.status == 'queued' or message.status == 'sent'):
        log.set_status(status=True, data=data)
    else:
        log.set_status(status=False, data=data)

    return data

