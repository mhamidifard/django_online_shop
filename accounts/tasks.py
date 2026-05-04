"""Celery tasks for accounts app - email notifications."""

import logging
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name='accounts.tasks.send_password_reset_email',
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_password_reset_email(self, user_email: str, reset_link: str):
    """
    Send password reset email asynchronously.
    
    Args:
        user_email: Recipient email address
        reset_link: Password reset URL
        
    Returns:
        dict: Task result with status and metadata
    """
    try:
        send_mail(
            subject="Password Reset Request",
            message=f"Use this link to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Password reset email sent successfully to {user_email}")
        return {
            'success': True,
            'recipient': user_email,
            'subject': 'Password Reset Request',
        }
    except Exception as exc:
        logger.exception(f"Failed to send password reset email to {user_email}")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name='accounts.tasks.send_welcome_email',
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_welcome_email(self, user_email: str, user_name: str):
    """
    Send welcome email to newly registered users.
    
    Args:
        user_email: Recipient email address
        user_name: User's display name
        
    Returns:
        dict: Task result with status and metadata
    """
    try:
        send_mail(
            subject="Welcome to Online Shop!",
            message=f"Hello {user_name},\n\nWelcome to our online shop! We're excited to have you as a customer.\n\nBest regards,\nThe Online Shop Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Welcome email sent successfully to {user_email}")
        return {
            'success': True,
            'recipient': user_email,
            'subject': 'Welcome to Online Shop!',
        }
    except Exception as exc:
        logger.exception(f"Failed to send welcome email to {user_email}")
        raise self.retry(exc=exc)
