from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.routers import router_responses
from app.lib.pda.api import OperationResponse

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    responses=router_responses,
)


# @router.post('/jobs', tags=['tasks'], response_model=OperationResponse)
async def create_job(request: Request) -> JSONResponse:
    from loguru import logger
    from worker import app as celery_app

    payload = await request.json()

    logger.warning(payload)

    response = OperationResponse(
        message=f'Scheduled the task "{payload["name"]}" for immediate execution.',
    )

    try:
        send_args = {}

        if 'id' in payload:
            send_args['task_id'] = payload['id']

        if 'args' in payload:
            send_args['args'] = payload['args']

        if 'kwargs' in payload:
            send_args['kwargs'] = payload['kwargs']

        if 'retries' in payload:
            send_args['retries'] = payload['retries']

        celery_app.send_task(payload['name'], **send_args)
    except Exception as e:
        response.success = False
        response.message = f'Failed to schedule the "{payload["name"]}" task for immediate execution: {e}.'

    return JSONResponse(response.model_dump(mode='json'))


@router.get('/conf', tags=['tasks'])
async def get_worker_configuration() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().conf()
    return JSONResponse(result)


@router.get('/stats', tags=['tasks'])
async def get_worker_stats() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().stats()
    return JSONResponse(result)


@router.get('/queues', tags=['tasks'])
async def get_worker_queues() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().active_queues()
    return JSONResponse(result)


@router.get('/status/reserved', tags=['tasks'])
async def get_tasks_by_status_reserved() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().reserved()
    return JSONResponse(result)


@router.get('/status/scheduled', tags=['tasks'])
async def get_tasks_by_status_scheduled() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().scheduled()
    return JSONResponse(result)


@router.get('/status/active', tags=['tasks'])
async def get_tasks_by_status_active() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().active()
    return JSONResponse(result)


@router.get('/status/revoked', tags=['tasks'])
async def get_tasks_by_status_revoked() -> JSONResponse:
    from worker import app as celery_app
    result = celery_app.control.inspect().revoked()
    return JSONResponse(result)


@router.get('/run/name/{name}', tags=['tasks'], response_model=OperationResponse)
async def run_by_name(name: str) -> JSONResponse:
    from worker import app as celery_app

    response = OperationResponse(
        message=f'Scheduled the task named "{name}" for immediate execution.',
    )

    try:
        send_args = {}
        celery_app.send_task(name, **send_args)
    except Exception as e:
        response.success = False
        response.message = f'Failed to schedule the "{name}" task for immediate execution: {e}.'

    return JSONResponse(response.model_dump(mode='json'))


@router.get('/run/key/{key}', tags=['tasks'], response_model=OperationResponse)
async def run_by_key(key: str) -> JSONResponse:
    from app import schedules
    from worker import app as celery_app

    response = OperationResponse(
        success=False,
        message=f'Could not locate a task schedule entry with the key "{key}".',
    )

    for schedule in schedules:
        if schedule.key is not None and schedule.key.lower() == key.lower():
            try:
                send_args = {}

                if schedule.args is not None:
                    send_args['args'] = schedule.args

                if schedule.kwargs is not None:
                    send_args['kwargs'] = schedule.kwargs

                celery_app.send_task(schedule.task, **send_args)

                response.success = True
                response.message = f'Scheduled the "{schedule.name}" task for immediate execution.'
            except Exception as e:
                response.success = False
                response.message = f'Failed to schedule the "{schedule.name}" task for immediate execution: {e}.'

    return JSONResponse(response.model_dump(mode='json'))


@router.get('/revoke/id/{id}', tags=['tasks'])
async def revoke_task_by_id(id: str) -> JSONResponse:
    from loguru import logger
    from worker import app as celery_app
    logger.debug(f'Revoking Celery task by id: {id}')
    celery_app.control.revoke(id)
    return JSONResponse({'success': True})


@router.get('/terminate/id/{id}', tags=['tasks'])
async def terminate_task_by_id(id: str) -> JSONResponse:
    from loguru import logger
    from worker import app as celery_app
    logger.debug(f'Terminating Celery task by id: {id}')
    celery_app.control.terminate(id)
    return JSONResponse({'success': True})


@router.get('/purge', tags=['tasks'])
async def purge_all_tasks() -> JSONResponse:
    from loguru import logger
    from worker import app as celery_app
    logger.debug(f'Purging all waiting Celery tasks...')
    celery_app.control.purge()
    return JSONResponse({'success': True})


@router.get('/broadcast/shutdown', tags=['tasks'])
async def broadcast_command_shutdown() -> JSONResponse:
    from loguru import logger
    from worker import app as celery_app
    logger.debug(f'Broadcasting worker shutdown command...')
    celery_app.control.broadcast('shutdown')
    return JSONResponse({'success': True})
