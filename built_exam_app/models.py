from django.db import models
import re
from datetime import datetime
# Create your models here.
class UserManager(models.Manager):
    def validator(self,postData):
        errors={}
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name'])<2:
            errors['first_name']='First name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name']='First name should only be letters'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name']='Last name should only be letters'
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']='Password should be at lesat 8 charictors'
        elif postData['password'] != postData['confirm_pw']:
                errors['password'] = 'Confirm PW does not match the password!'
        user=Users.objects.filter(email=postData['email'])
        if user:
            errors['email']='Email is already exist'
        return errors
class TripManager(models.Manager):
    def validator(self,postData):
        errors ={}
        today =datetime.today().date() 
        if len(postData['destination']) < 3:
            errors['destination'] = 'a trip destination must conists at least 3 character'
        if len(postData['plan']) < 1:
            errors['plan'] = 'a plan must be porvided'
        if len(postData['start_date']) < 1:
            errors['start_date'] = 'a start date must be porvided'
        elif postData['start_date'] < str(today):
            errors['start_date'] = 'start date must be in the future'
        if len(postData['end_date']) < 1:
            errors['end_date'] = 'a end date must be porvided'
        elif postData['end_date'] < str(today):
            errors['end_date'] = 'end date must be in the future'

        return errors
class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_by = models.ForeignKey(Users, related_name='trip_created', on_delete=models.CASCADE)
    users_who_join_trip=models.ManyToManyField(Users,related_name="book_trip")
    objects = TripManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)