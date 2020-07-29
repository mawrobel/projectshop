from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, commit=True):
        if not email:
            raise ValueError(_("Użytkownik musi mieć adres mailowy"))
        if not username:
            raise ValueError(_("Użytkownik musi mieć swoją nazwę"))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)

        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username=username,
            password=password,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True, default=None
    )
    username = models.CharField(_('username'), max_length=50, unique=True)
    password = models.CharField(_('password'), max_length=128, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    slug = models.SlugField(unique=True, max_length=100)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            "Określa, czy tego użytkownika należy traktować jako aktywnego. Usuń zaznaczenie, zamiast usuwać konta."
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            "„Wskazuje, czy użytkownik może zalogować się do tej witryny administratora."
        ),
    )

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now,
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_name(self):
        """
        get back name of user

        """
        return self.username

    def __str__(self):
        return "{}".format(self.get_name())

    def has_perm(self, perm, obj=None):
        " is User Admin ?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Is User can log in ?"
        # Simplest possible answer: Yes, always
        return True

    # def get_absolute_url(self):
    #   return reverse('LatarnikRP:profile', kwargs={"user_slug": str(self.slug)})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True)
    for_eighteen = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('ProjectShop:category',
                       args=[str(self.name)
                             ])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ParentChild(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="parent")
    child = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="child")
    objects = models.Manager()

    def __str__(self):
        return str(self.parent.name) + "/" + str(self.child.name)


class Product(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    for_eighteen = models.BooleanField(default=False)
    description = models.TextField(max_length=512)
    CONDITION_CHOICE = {
        ('USED', 'used'),
        ('NEW', 'new'),
    }
    condition = models.CharField(max_length=4,
                                 choices=CONDITION_CHOICE,
                                 default='NEW')

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('ProjectShop:product',
                       args=[self.category.slug,
                             self.slug
                             ])

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
