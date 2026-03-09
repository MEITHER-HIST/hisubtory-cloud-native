import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from accounts.models import User

def create_admin_user():
    email = "admin@admin.com"
    username = "admin"
    password = "admin1234"
    
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.save()
        print(f"User {username} updated.")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"User {username} created successfully.")

if __name__ == "__main__":
    create_admin_user()
