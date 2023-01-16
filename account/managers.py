from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, first_name, last_name, email, phone_no, password=None,):
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(  
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, phone_no, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_no = phone_no,
        )
        user.set_password(password),
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
        
        
        
        
        