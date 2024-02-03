from pda.celery import app as celery


@celery.task(name='pda.twilio.send_call')
def send_call(to_phone: str, message: str) -> bool:
    from loguru import logger
    from twilio.rest import Client
    from twilio.rest.api.v2010.account.call import CallInstance
    from twilio.twiml.voice_response import VoiceResponse
    from app import config

    response: VoiceResponse = VoiceResponse()

    # Introduce a delay before the call message is played if configured to do so
    try:
        if config.twilio.notification.call_delay > 0:
            response.pause(length=config.twilio.notification.call_delay)
    except AttributeError as e:
        pass

    response.say(message, voice=config.twilio.say.voice().ref, language=config.twilio.say.language().ref)

    client: Client = Client(config.twilio.account_sid().ref, config.twilio.auth_token().ref)

    try:
        result = client.calls.create(
            twiml=str(response),
            from_=config.twilio.from_phone().ref,
            to=to_phone,
        )
    except Exception as e:
        logger.error(f'Error sending text message: {e}')
        return False

    failed_statuses = [
        CallInstance.Status.FAILED,
        CallInstance.Status.BUSY,
        CallInstance.Status.NO_ANSWER,
        CallInstance.Status.CANCELED,
    ]

    if result.status in failed_statuses:
        logger.error(f'Call failed with status: {result.status}')
        return False

    return True


@celery.task(name='pda.twilio.send_text')
def send_text(to_phone: str, message: str) -> bool:
    from loguru import logger
    from twilio.rest import Client
    from twilio.rest.api.v2010.account.message import MessageInstance
    from app import config

    client: Client = Client(config.twilio.account_sid().ref, config.twilio.auth_token().ref)

    try:
        result = client.messages.create(
            body=message,
            from_=config.twilio.from_phone().ref,
            to=to_phone,
        )
    except Exception as e:
        logger.error(f'Error sending text message: {e}')
        return False

    failed_statuses = [
        MessageInstance.Status.FAILED,
        MessageInstance.Status.UNDELIVERED,
        MessageInstance.Status.CANCELED,
    ]

    if result.status in failed_statuses:
        logger.error(f'Call failed with status: {result.status}')
        return False

    return True
