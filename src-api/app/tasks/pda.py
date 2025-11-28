from celery import current_app
from typing import Any
from app.lib.enums import TaskEnum
from app.lib.mail import EmailSendResult


@current_app.task(name=TaskEnum.PDA_MAIL.value, label='PDA Mail',
                  autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 300})
def mail(individual_tasks: bool = True, **kwargs) -> EmailSendResult:
    """This task builds an email based on the given arguments and sends it to the defined recipient(s)."""
    import jsonpickle
    import time
    from loguru import logger
    from worker import app as celery_app
    from app.lib.mail import Email

    if 'mail_to' not in kwargs:
        raise Exception('Mail recipient(s) not provided!')

    if not isinstance(kwargs['mail_to'], list) and not isinstance(kwargs['mail_to'], str):
        raise Exception(f'Mail recipient(s) not valid: Type: {type(kwargs["mail_to"])}, Value: {kwargs["mail_to"]}')

    if isinstance(kwargs['mail_to'], str):
        kwargs['mail_to'] = [kwargs['mail_to']]

    log_msg = 'Sending mail:\n'

    if 'mail_from' in kwargs:
        log_msg += f'From: {kwargs["mail_from"]}\n'

    log_msg += f'To: {kwargs["mail_to"]}\n'

    if 'subject' in kwargs:
        log_msg += f'Subject: {kwargs["subject"]}\n'

    if 'template' in kwargs:
        log_msg += f'Template: {kwargs["template"]}\n'
        if 'data' in kwargs:
            if isinstance(kwargs['data'], str):
                log_msg += f'Data: {jsonpickle.loads(kwargs["data"])}\n\n'
            elif kwargs['data'] is not None:
                log_msg += f'Data: {kwargs["data"]}\n\n'

    if 'body_html' in kwargs:
        log_msg += f'Body [HTML]:\n{kwargs["body_html"]}\n\n'

    if 'body_text' in kwargs:
        log_msg += f'Body [PLAIN]:\n{kwargs["body_text"]}\n\n'

    logger.debug(log_msg)

    if not individual_tasks:
        send_result = Email(**kwargs).send()
    else:
        tasks = []

        for to in kwargs['mail_to']:
            send_kwargs = {**kwargs, 'mail_to': to}
            tasks.append(celery_app.send_task(TaskEnum.PDA_MAIL_SEND.value, kwargs=send_kwargs))

        logger.debug(f'Waiting for {len(tasks)} mail sub-tasks to complete...')

        while not all(task.ready() for task in tasks):
            time.sleep(1)

        send_result = EmailSendResult()

        for task in tasks:
            send_result.responses += task.result.responses

        logger.debug(f'All {len(tasks)} mail sub-tasks completed.')

    logger.debug(f'Finished sending mail.')

    for response in send_result.responses:
        logger.debug(f'Mail Send Response: Recipient: {response.recipient}, Status: {response.success}. '
                     + f'Code: {response.code}, Message: {response.message}')

    return send_result


@current_app.task(name=TaskEnum.PDA_MAIL_SEND.value, label='PDA Mail Send',
                  autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 300})
def mail_send(**kwargs) -> EmailSendResult:
    """This task builds an email based on the given arguments and sends it to the defined recipient(s)."""
    from loguru import logger
    from app.lib.mail import Email

    logger.debug(f'Sending mail: {kwargs}')

    send_result = Email(**kwargs).send()

    logger.debug(f'Finished sending mail.')

    return send_result


@current_app.task(name=TaskEnum.PDA_ALERT.value, label='PDA Alert')
def alert(msg: str, info: Any = None, title: str = None):
    """Sends an alert to the configured administrators about runtime issues."""
    from app import notifications
    from app.lib.notifications import NotificationManager
    from app.lib.notifications.events import AlertEvent

    message = msg.strip()

    if isinstance(info, str):
        message += f'\n\nInfo:\n{info}'

    event = AlertEvent(
        title=title,
        message=message,
        exception=info,
    )

    NotificationManager(configs=notifications).handle_event(event)


@current_app.task(name=TaskEnum.PDA_TEST.value, label='PDA Test Task')
def test():
    """Sends a log message to indicate task execution."""
    import time
    from loguru import logger
    logger.warning(f'Starting test task.')
    time.sleep(1)
    logger.warning(f'Finished test task.')


@current_app.task(name=TaskEnum.PDA_TEST_MAIL.value, label='PDA Test Mail')
def test_mail():
    """Sends an alert message to test the mailing system."""
    from loguru import logger
    from worker import app as celery_app
    logger.warning(f'Starting mail test task.')
    celery_app.send_task(TaskEnum.PDA_ALERT.value, kwargs={
        'msg': 'PDA Mail Test',
        'info': 'This is an PDA mailing system test.'
    })
    logger.warning(f'Finished mail test task.')


@current_app.task(name=TaskEnum.PDA_TEST_EXCEPTION.value, label='PDA Test Exception')
def test_exception():
    """Throws an exception immediately to test global exception handling."""
    raise Exception('Test Exception')


@current_app.task(name=TaskEnum.PDA_TEST_EXCEPTION_RETRY.value, label='PDA Test Exception Retry',
                  autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'countdown': 20})
def test_exception_retry():
    """Throws an exception immediately to test auto-retry handling."""
    raise Exception('Test Exception')


@current_app.task(name=TaskEnum.PDA_TEST_DELAY.value, label='PDA Test Delay')
def test_delay():
    """Executes a pause to simulate a long-running task."""
    import time
    from loguru import logger
    logger.warning(f'Starting test delay task.')
    time.sleep(60)
    logger.warning(f'Finished test delay task.')
