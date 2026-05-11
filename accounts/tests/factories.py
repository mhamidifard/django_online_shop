import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    # By default, factory_boy won't hash passwords correctly if we just pass password='...'.
    # PostGenerationMethodCall is a clean way to hash it after instance creation.
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_active = True
