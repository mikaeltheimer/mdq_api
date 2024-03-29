from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from uuid import uuid4


class MDQUserManager(BaseUserManager):
    '''Updates the base user manager to provide some additional functionality'''
    def create_user(self, email, first_name, last_name, username=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name, username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, username):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, first_name, last_name, username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MDQUser(AbstractBaseUser):
    '''Custom user account, specific to MDQ spec'''

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)

    # A unique username
    username = models.CharField(max_length=255, unique=True)

    # User personal information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    fb_token = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.FileField(upload_to='motsditsv2/avatars', null=True, blank=True)

    # Access control information
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Social information
    likes = models.ManyToManyField('motsdits.MotDit', null=True, blank=True, related_name='likes')
    favourites = models.ManyToManyField('motsdits.MotDit', null=True, blank=True, related_name='favourites')

    liked_photos = models.ManyToManyField('motsdits.Photo', null=True, blank=True, related_name='likes')
    liked_stories = models.ManyToManyField('motsdits.Story', null=True, blank=True, related_name='likes')

    following = models.ManyToManyField('MDQUser', null=True, blank=True, related_name='followers')

    validation_code = models.CharField(max_length=255, null=True, blank=True, default=lambda: uuid4().hex)
    validated = models.BooleanField(default=False)

    # Other requirements
    objects = MDQUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
