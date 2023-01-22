from django.contrib.auth.models import BaseUserManager

class FirstManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, location, designation, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        email=self.normalize_email(email)
        user=self.model(username=username, email=email, first_name=first_name, last_name=last_name, location=location, designation=designation, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, first_name, last_name, location, designation, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_user(username, email, first_name, last_name, location, designation, password, **extra_fields)