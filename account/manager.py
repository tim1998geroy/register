from django.contrib.auth.base_user import BaseUserManager

from .send_email import send_activation_email

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.create_activation_code()
        send_activation_email(user.email, user.activation_code)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('il_staff', True)
        extra_fields.setdefault('il_activve', True)
        extra_fields.setdefault('il_superuser', True)
        return self.create_user(email, password, **extra_fields)
        