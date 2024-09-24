from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ResultAnswersModel(models.Model):
    user_id = models.ForeignKey('base_user.MyUser',
                                            on_delete=models.CASCADE, related_name='user')
    question_name = models.CharField(verbose_name="Questions",max_length=255)
    answer_name = models.CharField(max_length=100)
    weight_number = models.DecimalField(max_digits=9, decimal_places=4)
    weight_type = models.CharField(max_length=30)

    def __str__(self):
        return f'Weight type:{self.weight_type} -- User:{self.user_id}/Question:{self.question_name}/ Answer: {self.answer_name}'



class MyUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser,PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    fullname = models.CharField(_("full name"), max_length=255, blank=True)
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, db_index=True
    )
    age = models.CharField(_("age"), max_length=3, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin " "site."),
        db_index=True,
    )
    is_superuser = models.BooleanField(
        _("Super user"),
        default=False,
        help_text=_("Designates whether the user can log into this admin " "site."),
        db_index=True,
    )
    total_score = models.DecimalField(max_digits=9,
                                        decimal_places=4,
                                        default=0.0)
    old_psw_hash = models.CharField(blank=True, null=True, max_length=300)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    """
        Important non-field stuff
    """
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        permissions = (
            ("can_see_staff_menu", "Can see Application menu on staff admin"),
            ("can_view_warehouse_panel", "Can use Warehouse panel"),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{full_name}".format(
            full_name=self.fullname,
        )


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)