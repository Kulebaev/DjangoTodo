from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
    
class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)  
    comment = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Здесь изменяем UserProfile на User
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Task {self.id} for {self.comment}"
