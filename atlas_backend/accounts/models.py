from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model for Atlas application.
    Extends Django's AbstractUser to add additional fields.
    """
    # User roles
    ROLE_ADMIN = 'admin'
    ROLE_EMPLOYEE = 'employee'
    ROLE_LEARNER = 'learner'
    
    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_EMPLOYEE, 'Employee'),
        (ROLE_LEARNER, 'Learner'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_LEARNER)
    is_admin = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    notification_preferences = models.JSONField(default=dict, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Using email as the username field for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username still required for admin

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """
        Returns the user's full name or username if no name is set
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure is_admin field is in sync with role
        """
        if self.role == self.ROLE_ADMIN:
            self.is_admin = True
        else:
            self.is_admin = False
        super().save(*args, **kwargs)
