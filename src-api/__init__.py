from __future__ import absolute_import, unicode_literals
from .worker import app as celery_app
__all__ = ('celery_app',)