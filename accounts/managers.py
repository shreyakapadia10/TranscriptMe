from django.contrib.auth.models import BaseUserManager

# Create your managers here.

class MyUserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **fields):
        if not email:
            raise ValueError('The User Must Provide Email-ID')

        user = self.model(
            email=self.normalize_email(email), # It converts letters to lower case if uppercase is provided
           **fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **fields):
        user = self.create_user(
            email=self.normalize_email(email), 
            password=password,
            **fields,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
