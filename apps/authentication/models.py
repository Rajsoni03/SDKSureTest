from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = email.lower().strip()
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "SUPER_ADMIN")
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    NORMAL_USER = "NORMAL_USER"

    ROLE_CHOICES = [
        (SUPER_ADMIN, "Super Administrator"),
        (ADMIN, "Administrator"),
        (NORMAL_USER, "Normal User"),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
        verbose_name="username",
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="first name")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="last name")
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=NORMAL_USER, db_index=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(
        default=False,
        verbose_name="staff status",
        help_text="Designates whether the user can log into this admin site.",
    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="date joined")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    login_count = models.IntegerField(default=0)

    # Override PermissionsMixin fields to avoid reverse accessor clash with auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="authentication_user_set",
        related_query_name="authentication_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="authentication_user_set",
        related_query_name="authentication_user",
    )

    assigned_boards = models.ManyToManyField(
        "devices.Board",
        blank=True,
        through="UserBoardAssignment",
        through_fields=("user", "board"),
        related_name="assigned_users",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class UserBoardAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey("devices.Board", on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="assignments_made",
    )

    class Meta:
        ordering = ["-assigned_at"]
        unique_together = [("user", "board")]
