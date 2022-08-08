from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Provide email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, default=None, on_delete=models.CASCADE, null=True, related_name='usergroup')
    phone = models.PositiveIntegerField(null=True)
    email = models.EmailField(unique=True, verbose_name='login')
    final_score = models.PositiveIntegerField(default=0, blank=True, null=True)
    rating_place = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    group_rating_place = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)
    tests_passed = models.IntegerField(default=0, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    #
    # class Meta:
    #     proxy = True
    #     ordering = ['-final_score']
    #     indexes = [
    #         models.Index(fields=['rating_place',]),
    #         models.Index(fields=['group_rating_place',]),
    #     ]

    def _str_(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(12, allowed_chars='1234567890#$%!?_')
        self.activation_code = code
        self.save()

    @staticmethod
    def set_rating_place():
        users = User.objects.all().order_by('-final_score')
        for i in range(len(users)):
            users[i].rating_place = i + 1
            users[i].save()

    def set_group_rating_place(self):
        users = User.objects.filter(group=self.group).order_by('-final_score')
        for i in range(len(users)):
            users[i].group_rating_place = i + 1
            users[i].save()

    def set_tests_passed(self, n):
        self.tests_passed += n
        self.save()

    def set_final_score(self, score):
        self.final_score += score
        self.save()

        # indexes = [
        #     models.Index(fields=['rating_place', ]),
        #     models.Index(fields=['group_rating_place', ]),
        # ]


class MyUser(User):
    class Meta:
        ordering = ['-final_score']
        proxy = True
        verbose_name = 'Leaderboard'
        verbose_name_plural = 'Leaderboard'

