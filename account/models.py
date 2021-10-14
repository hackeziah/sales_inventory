import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group, AbstractUser, UserManager as OldUserManager
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe


def codeGenerator():
    return f'{uuid.uuid4().hex[:8].lower()}'


def name_path_file(path, filename):
    import uuid
    uuid_for_filename = uuid.uuid4().hex[:6]
    filename = "{uuid}-{filename}".format(
        uuid=uuid_for_filename,
        filename=filename,
    )
    return '/'.join([path, filename])


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(OldUserManager):
    pass


class Account(AbstractUser, BaseModel):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    objects = UserManager()


def upload_to_profile(instance, filename):
    return name_path_file('images/profile', filename)


class Profile(BaseModel):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    profile = models.ImageField(upload_to=upload_to_profile, default="images/profile/default.jpg")
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    email = models.EmailField(max_length=100, verbose_name='Email Address')
    contact_no = models.CharField(max_length=168, null=True, blank=True)

    user = models.OneToOneField(
        to=Account, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    @property
    def picture_preview(self):
        if self.profile:
            return mark_safe('<img src="{}" width="200" height="200" />'.format(self.profile.url))
        return "Not Yet Set"

    def save(self, *args, **kwargs):
        if self.user is None:
            if Account.objects.filter(email=self.email).exists():
                raise ValidationError("Email is already Exist")

            if Account.objects.filter(username=self.email).exists():
                raise ValidationError("Username is already Exist")

            self.first_name = self.first_name.upper()
            self.last_name = self.last_name.upper()
            password = codeGenerator().lower().replace(" ", "")
            user = Account.objects.create_user(is_staff=True, username=self.email, password=password,
                                               email=self.email,
                                               first_name=self.first_name, last_name=self.last_name, )
            self.user = user
            user.save()
            super(Profile, self).save(*args, **kwargs)

        try:
            obj = Account.objects.get(pk=self.user.pk)
            obj.email = self.email
            obj.username = self.email
            obj.save()
        except Account.DoesNotExist:
            raise ValidationError("Account Does Not Exist")

        super(Profile, self).save(*args, **kwargs)
