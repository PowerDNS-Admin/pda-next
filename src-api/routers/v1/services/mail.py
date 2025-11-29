import uuid
from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from lib.pda.api.services.mail import MailServiceSendRequest, MailServiceSendResponse
from routers.root import router_responses

router = APIRouter(
    prefix='/mail',
    tags=['services'],
    responses=router_responses,
)

responses = {
    200: {
        'description': 'Mail request sent.',
        'content': {
            'application/json': {
                'example': {
                    'id': uuid.uuid4(),
                    'status': 'sent',
                    'message': 'Mail request completed.',
                    'responses': [
                        {'recipient': 'Recipient #1 <recipient1@domain.com>', 'success': True, 'code': 250},
                        {'recipient': 'Recipient #2 <recipient2@domain.com>', 'success': False, 'code': 450,
                         'message': 'This mailbox is unavailable.'},
                        {'recipient': 'recipient3@domain.com', 'success': True, 'code': 250},
                    ],
                },
            },
        },
    },
    202: {
        'description': 'Mail request queued.',
        'content': {
            'application/json': {
                'example': {
                    'id': uuid.uuid4(),
                    'status': 'queued',
                    'message': 'Mail request queued.',
                },
            },
        },
    },
    500: {
        'description': 'Mail request failed.',
        'content': {
            'application/json': {
                'example': {
                    'id': uuid.uuid4(),
                    'status': 'failed',
                    'message': 'Mail request failed.',
                },
            },
        },
    },
}


def update_response_from_task(response: MailServiceSendResponse, task: AsyncResult) -> tuple[
    MailServiceSendResponse, int]:
    """Updates the given response object with appropriate information based on the state of the given task."""

    response.status = 'queued'
    response.message = 'Mail request queued.'
    status_code = 202
    state = task.state

    if state == 'STARTED':
        response.status = 'sending'
        response.message = 'Mail request sending.'

    if state == 'RETRY':
        response.status = 'retry'
        response.message = 'Mail request pending retry.'

    if state == 'SUCCESS':
        response.status = 'sent'
        response.message = 'Mail request completed.'
        response.responses = task.result.responses
        status_code = 200

    if state == 'FAILURE':
        response.status = 'failed'
        response.message = 'Mail request failed.'
        status_code = 500

    return response, status_code


@router.post('/send', response_model=MailServiceSendResponse, responses=responses)
async def send(request: MailServiceSendRequest, wait_for_finish: bool = False, timeout: float = 60) -> JSONResponse:
    import time
    from loguru import logger
    from lib.enums import TaskEnum
    from worker import app as celery_app

    response = MailServiceSendResponse()

    try:
        logger.debug(f'Queueing mail request: {request}')

        task: AsyncResult = celery_app.send_task(TaskEnum.PDA_MAIL.value, kwargs={
            'mail_from': request.from_address,
            'mail_to': request.to_addresses,
            'mail_cc': request.cc_addresses,
            'subject': request.subject,
            'body_html': request.body_html,
            'body_text': request.body_plain,
        })

        response.id = uuid.UUID(task.id)

        if wait_for_finish:
            start = time.time()
            while time.time() - start < timeout:
                time.sleep(1)
                if task.ready():
                    break

        response, status_code = update_response_from_task(response, task)

        return JSONResponse(response.model_dump(mode='json'), status_code=status_code)

    except Exception as e:
        logger.error(f'Mail request failed:\n{e}')

        response.status = 'failed'
        response.message = 'Mail request failed.'

        return JSONResponse(response.model_dump(mode='json'), status_code=500)


@router.get('/status/:id', response_model=MailServiceSendResponse, responses=responses)
async def status(id: uuid.UUID) -> JSONResponse:
    from worker import app as celery_app

    response = MailServiceSendResponse(id=id)

    task = AsyncResult(id=str(id), app=celery_app)

    response.status = 'queued'
    response.message = 'Mail request queued.'
    status_code = 202
    state = task.state

    if state == 'STARTED':
        response.status = 'sending'
        response.message = 'Mail request sending.'

    if state == 'RETRY':
        response.status = 'retry'
        response.message = 'Mail request pending retry.'

    if state == 'SUCCESS':
        response.status = 'sent'
        response.message = 'Mail request completed.'
        response.responses = task.result.responses
        status_code = 200

    if state == 'FAILURE':
        response.status = 'failed'
        response.message = 'Mail request failed.'
        status_code = 500

    return JSONResponse(response.model_dump(mode='json'), status_code=status_code)
