from fastapi import FastAPI


def install_routers(app: FastAPI) -> None:
    """Attach local and global routers"""
    from app import config
    from lib.config.app import EnvironmentEnum
    from routers import api, dev, root
    from routers import v1

    # Attach API router to root router
    # root.router.include_router(api.router)

    # Attach API V1 router to root router
    root.router.include_router(v1.router)

    # Dev Router
    if config.app.environment.name in (EnvironmentEnum.local, EnvironmentEnum.dev):
        root.router.include_router(dev.router)

    # Attach root router to app
    app.include_router(root.router)
