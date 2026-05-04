"""Base Celery configuration shared across all environments."""

import os


def get_env(name: str, default: str | None = None) -> str | None:
    """Get environment variable with optional default."""
    return os.getenv(name, default)


def get_int_env(name: str, default: int) -> int:
    """Get integer environment variable with default."""
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return default
    return int(raw_value)


# Broker and Result Backend
CELERY_BROKER_URL = get_env('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_RESULT_BACKEND = get_env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Task serialization
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# Task execution settings
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = get_int_env('CELERY_TASK_TIME_LIMIT', 300)  # 5 minutes hard limit
CELERY_TASK_SOFT_TIME_LIMIT = get_int_env('CELERY_TASK_SOFT_TIME_LIMIT', 240)  # 4 minutes soft limit
CELERY_TASK_ACKS_LATE = True  # Acknowledge task after completion
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Fetch one task at a time

# Result backend settings
CELERY_RESULT_EXPIRES = get_int_env('CELERY_RESULT_EXPIRES', 3600)  # 1 hour
CELERY_RESULT_PERSISTENT = True

# Retry settings
CELERY_TASK_DEFAULT_MAX_RETRIES = 3
CELERY_TASK_DEFAULT_RETRY_DELAY = 60  # 60 seconds

# Priority queues configuration
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_PRIORITY = 5

# Define queues with priorities
CELERY_TASK_QUEUES = {
    'critical': {
        'exchange': 'critical',
        'routing_key': 'critical',
        'priority': 10,
    },
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
        'priority': 5,
    },
    'low': {
        'exchange': 'low',
        'routing_key': 'low',
        'priority': 1,
    },
}

# Task routing
CELERY_TASK_ROUTES = {
    'accounts.tasks.send_password_reset_email': {'queue': 'critical', 'priority': 10},
    'accounts.tasks.send_welcome_email': {'queue': 'default', 'priority': 5},
    'orders.tasks.send_order_confirmation_email': {'queue': 'critical', 'priority': 10},
    'orders.tasks.send_order_status_update_email': {'queue': 'default', 'priority': 5},
}

# Worker settings
CELERY_WORKER_MAX_TASKS_PER_CHILD = get_int_env('CELERY_WORKER_MAX_TASKS_PER_CHILD', 1000)
CELERY_WORKER_DISABLE_RATE_LIMITS = False

# Monitoring
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_SEND_TASK_ERROR_EMAILS = False  # Set to True in production with proper email config
