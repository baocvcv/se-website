""" Base model for User """
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from .profile import Profile

class User(AbstractUser):
    """ Extending AbstractUser to create custom User

    Attributes:
    """
    STUDENT = 'Student'
    ADMIN = 'Admin'
    SUPER_ADMIN = 'SuperAdmin'
    USER_GROUP_CHOICES = [
        ('Student', 'Student'),
        ('Admin', 'Admin'),
        ('SuperAdmin', 'SuperAdmin'),
    ]
    user_group = models.CharField(
        max_length=10,
        choices=USER_GROUP_CHOICES,
        default=STUDENT,
    )

    last_login_time = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True)

    is_banned = models.BooleanField(default=False)

    user_permissions = models.ForeignKey('UserPermissions', on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # quesiton banks owned by the user
    question_banks = ArrayField(models.IntegerField())

    def __str__(self):
        "Stringify"
        return self.username + "(%s)" % self.email
