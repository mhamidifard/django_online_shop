#!/usr/bin/env python
"""
Test script to verify Celery setup and configuration.
Run this after installing dependencies but before starting workers.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings.development')
django.setup()

from celery import current_app
from accounts.tasks import send_password_reset_email, send_welcome_email
from orders.tasks import send_order_confirmation_email, send_order_status_update_email


def test_celery_app():
    """Test Celery app is properly configured."""
    print("=" * 70)
    print("Testing Celery Application Configuration")
    print("=" * 70)
    
    app = current_app
    print(f"✓ Celery app name: {app.main}")
    print(f"✓ Broker URL: {app.conf.broker_url}")
    print(f"✓ Result backend: {app.conf.result_backend}")
    print(f"✓ Task serializer: {app.conf.task_serializer}")
    print(f"✓ Result serializer: {app.conf.result_serializer}")
    print(f"✓ Timezone: {app.conf.timezone}")
    print()


def test_task_registration():
    """Test that all tasks are properly registered."""
    print("=" * 70)
    print("Testing Task Registration")
    print("=" * 70)
    
    app = current_app
    registered_tasks = sorted(app.tasks.keys())
    
    expected_tasks = [
        'accounts.tasks.send_password_reset_email',
        'accounts.tasks.send_welcome_email',
        'orders.tasks.send_order_confirmation_email',
        'orders.tasks.send_order_status_update_email',
    ]
    
    print(f"Total registered tasks: {len(registered_tasks)}")
    print()
    
    for task_name in expected_tasks:
        if task_name in registered_tasks:
            print(f"✓ {task_name}")
        else:
            print(f"✗ {task_name} - NOT FOUND!")
    
    print()


def test_task_routing():
    """Test task routing configuration."""
    print("=" * 70)
    print("Testing Task Routing Configuration")
    print("=" * 70)
    
    app = current_app
    routes = app.conf.task_routes
    
    if routes:
        print("Task routes configured:")
        for pattern, config in routes.items():
            print(f"  {pattern} → {config}")
    else:
        print("✗ No task routes configured!")
    
    print()


def test_queue_configuration():
    """Test queue configuration."""
    print("=" * 70)
    print("Testing Queue Configuration")
    print("=" * 70)
    
    app = current_app
    
    print(f"Default queue: {app.conf.task_default_queue}")
    print(f"Default priority: {app.conf.task_default_priority}")
    
    if hasattr(app.conf, 'task_queues') and app.conf.task_queues:
        print("\nConfigured queues:")
        for queue_name, queue_config in app.conf.task_queues.items():
            print(f"  {queue_name}:")
            print(f"    - Exchange: {queue_config.get('exchange')}")
            print(f"    - Routing key: {queue_config.get('routing_key')}")
            print(f"    - Priority: {queue_config.get('priority')}")
    
    print()


def test_task_settings():
    """Test task execution settings."""
    print("=" * 70)
    print("Testing Task Execution Settings")
    print("=" * 70)
    
    app = current_app
    
    print(f"Task time limit: {app.conf.task_time_limit}s")
    print(f"Task soft time limit: {app.conf.task_soft_time_limit}s")
    print(f"Task acks late: {app.conf.task_acks_late}")
    print(f"Worker prefetch multiplier: {app.conf.worker_prefetch_multiplier}")
    print(f"Result expires: {app.conf.result_expires}s")
    print(f"Task track started: {app.conf.task_track_started}")
    print()


def test_task_signatures():
    """Test that tasks can be called (without executing)."""
    print("=" * 70)
    print("Testing Task Signatures")
    print("=" * 70)
    
    try:
        # Test password reset email signature
        sig1 = send_password_reset_email.s('test@example.com', 'http://example.com/reset')
        print(f"✓ send_password_reset_email signature: {sig1}")
        
        # Test welcome email signature
        sig2 = send_welcome_email.s('test@example.com', 'Test User')
        print(f"✓ send_welcome_email signature: {sig2}")
        
        # Test order confirmation signature
        sig3 = send_order_confirmation_email.s('test@example.com', 123, '$99.99')
        print(f"✓ send_order_confirmation_email signature: {sig3}")
        
        # Test order status update signature
        sig4 = send_order_status_update_email.s('test@example.com', 123, 'PENDING', 'SHIPPED')
        print(f"✓ send_order_status_update_email signature: {sig4}")
        
        print("\n✓ All task signatures created successfully!")
    except Exception as e:
        print(f"\n✗ Error creating task signatures: {e}")
    
    print()


def test_imports():
    """Test that all necessary modules can be imported."""
    print("=" * 70)
    print("Testing Module Imports")
    print("=" * 70)
    
    try:
        import celery
        print(f"✓ celery version: {celery.__version__}")
        
        import redis
        print(f"✓ redis version: {redis.__version__}")
        
        import kombu
        print(f"✓ kombu version: {kombu.__version__}")
        
        import django_celery_results
        print(f"✓ django_celery_results installed")
        
        try:
            import flower
            print(f"✓ flower installed")
        except ImportError:
            print("✗ flower not installed (optional)")
        
        print("\n✓ All required modules imported successfully!")
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
    
    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "CELERY SETUP VERIFICATION" + " " * 28 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    try:
        test_imports()
        test_celery_app()
        test_task_registration()
        test_task_routing()
        test_queue_configuration()
        test_task_settings()
        test_task_signatures()
        
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print("✓ Celery setup verification completed successfully!")
        print()
        print("Next steps:")
        print("  1. Install RabbitMQ and Redis (see CELERY_QUICKSTART.md)")
        print("  2. Run migrations: python manage.py migrate")
        print("  3. Start Celery worker: celery -A online_shop worker -l info")
        print("  4. Start Django: python manage.py runserver")
        print("  5. Test by triggering password reset or creating an order")
        print()
        
        return 0
        
    except Exception as e:
        print("=" * 70)
        print("ERROR")
        print("=" * 70)
        print(f"✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
