from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "coderank",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_routes = {
    "app.workers.execution_worker.execute_submission_task": {
        "queue": "execution_queue",
    },
}

import app.workers.execution_worker