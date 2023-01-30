from celery import Celery

from config import conf_redis
from services.azure_service import AzureService

celery_app = Celery(
    "tasks",
    broker=f'redis://{conf_redis.REDIS_HOST}:{conf_redis.REDIS_PORT}/{conf_redis.REDIS_DB}',
    backend=f'redis://{conf_redis.REDIS_HOST}:{conf_redis.REDIS_PORT}/{conf_redis.REDIS_DB}',
)

celery_app.conf.event_serializer = 'pickle'
celery_app.conf.task_serializer = 'pickle'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['application/json', 'application/x-python-serialize']


def get_service():
    return AzureService()


@celery_app.task
def upload_data(filename: str, data: bytes, service=get_service()):
    return service.upload_file(filename, data)


@celery_app.task
def download_data(filename: str, service=get_service()):
    return service.download_file(filename)