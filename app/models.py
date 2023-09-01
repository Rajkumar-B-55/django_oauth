from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Base(models.Model):
    pid = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True  # The abstract = True attribute makes Base an abstract model.


class User(Base, AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'  # db_table attribute in the Meta class to specify the table name explicitly if needed.

    @classmethod
    def get_by_username(cls, email):
        try:
            user = cls.objects.get(email=email)
            return user
        except cls.DoesNotExist:
            return None
