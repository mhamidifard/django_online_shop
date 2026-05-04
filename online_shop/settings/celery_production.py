"""Celery configuration for production environment."""

from .celery_base import *
import os

# Production broker and backend (should be set via environment variables)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

# Broker connection settings for production
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10

# Security settings
CELERY_BROKER_USE_SSL = os.getenv('CELERY_BROKER_USE_SSL', 'False').lower() == 'true'
CELERY_REDIS_BACKEND_USE_SSL = os.getenv('CELERY_REDIS_BACKEND_USE_SSL', 'False').lower() == 'true'

# Production logging
CELERY_WORKER_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'

# Send task error emails in production
CELERY_SEND_TASK_ERROR_EMAILS = True

# Performance tuning for production
CELERY_WORKER_PREFETCH_MULTIPLIER = 4
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

# Task compression
CELERY_TASK_COMPRESSION = 'gzip'
CELERY_RESULT_COMPRESSION = 'gzip'
