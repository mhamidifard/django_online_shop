"""Celery tasks for orders app - email notifications."""

import logging
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name='orders.tasks.send_order_confirmation_email',
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_order_confirmation_email(self, user_email: str, order_id: int, total_amount: str):
    """
    Send order confirmation email asynchronously.
    
    Args:
        user_email: Recipient email address
        order_id: Order ID
        total_amount: Total order amount
        
    Returns:
        dict: Task result with status and metadata
    """
    try:
        send_mail(
            subject=f"Order Confirmation - Order #{order_id}",
            message=f"Thank you for your order!\n\nOrder ID: #{order_id}\nTotal Amount: {total_amount}\n\nWe'll send you another email when your order ships.\n\nBest regards,\nThe Online Shop Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Order confirmation email sent successfully to {user_email} for order #{order_id}")
        return {
            'success': True,
            'recipient': user_email,
            'subject': f'Order Confirmation - Order #{order_id}',
            'order_id': order_id,
        }
    except Exception as exc:
        logger.exception(f"Failed to send order confirmation email to {user_email} for order #{order_id}")
        raise self.retry(exc=exc)


@shared_task(
    bind=True,
    name='orders.tasks.send_order_status_update_email',
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_order_status_update_email(self, user_email: str, order_id: int, old_status: str, new_status: str):
    """
    Send order status update email asynchronously.
    
    Args:
        user_email: Recipient email address
        order_id: Order ID
        old_status: Previous order status
        new_status: New order status
        
    Returns:
        dict: Task result with status and metadata
    """
    try:
        send_mail(
            subject=f"Order Status Update - Order #{order_id}",
            message=f"Your order status has been updated.\n\nOrder ID: #{order_id}\nPrevious Status: {old_status}\nNew Status: {new_status}\n\nBest regards,\nThe Online Shop Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Order status update email sent successfully to {user_email} for order #{order_id}")
        return {
            'success': True,
            'recipient': user_email,
            'subject': f'Order Status Update - Order #{order_id}',
            'order_id': order_id,
            'new_status': new_status,
        }
    except Exception as exc:
        logger.exception(f"Failed to send order status update email to {user_email} for order #{order_id}")
        raise self.retry(exc=exc)
