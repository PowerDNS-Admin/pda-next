from fastapi import APIRouter, Response, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from lib.api.dependencies import get_db_session
from models.api.auth import UserSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/auth',
    responses=router_responses,
)


@router.post('/login', response_model=UserSchema)
async def login(
        response: Response,
        session:AsyncSession = Depends(get_db_session),
        username: str = Form(...),
        password: str = Form(...),
) -> UserSchema:
    from lib.security import COOKIE_NAME
    from models.db.auth import UserStatusEnum, User, Session

    # Delete any existing session cookie
    # FIXME: The following cookie delete isn't functioning
    response.delete_cookie(COOKIE_NAME, path='/')

    if not username or isinstance(username, str) and not len(username.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No username provided.')

    if not password or isinstance(password, str) and not len(password.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No password provided.')

    # TODO: Implement tenant segregation

    # Attempt to retrieve a user from the database based on the given username
    db_user = await User.get_by_username(session, username)

    if not db_user or not db_user.verify_password(password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid credentials provided.')

    # Ensure that the user has an appropriate status
    if db_user.status != UserStatusEnum.active:
        reason = 'This user is not active.'

        if db_user.status == UserStatusEnum.pending:
            reason = 'This user has not yet been invited.'

        if db_user.status == UserStatusEnum.invited:
            reason = 'This user has not yet been confirmed.'

        if db_user.status == UserStatusEnum.suspended:
            reason = 'This user has been suspended.'

        if db_user.status == UserStatusEnum.disabled:
            reason = 'This user has been disabled.'

        raise HTTPException(status.HTTP_401_UNAUTHORIZED, reason)

    # Create the user schema from the database user
    user = UserSchema.model_validate(db_user)

    # TODO: Create a secure session cookie mechanism

    # Create a new auth session for the user
    auth_session = await Session.create_session(session, user)

    response.set_cookie(
        key=COOKIE_NAME,
        value=auth_session.id.hex,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    return user
