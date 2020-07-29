from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {} # empty dictionary for any errors
        # first and last name  should be at least 2 characters
        if len(post_data['first_name']) < 2:
            errors['first_name']  = "First name should be at least 2 characters"
        # network should be at least 3 characters
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        # only alphabetic characters...not is the same as !=...just cleaner
        if not post_data['first_name'].isalpha() and post_data['last_name'].isalpha():
            errors['letters'] = "Letters only, no numbers are allowed here!"
        # email validation
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        # password
        if len(post_data['password']) < 8:
            errors['password'] = "Password should contain at least 8 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobManager(models.Manager):
    def job_validator(self,postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title should be at least 3 characters"
        if len(postData['description']) < 10:
            errors['description'] = "Description should be at least 10 characters"
        if len(postData['location']) < 1:
            errors['location'] = "Location should not be left blank"
        return errors
    
    def edit_job_validator(self,postData):
        errors = {}
        if len(postData['edit_title']) < 3:
            errors['edit_title'] = " Title should be at least 3 characters"
        if len(postData['edit_description']) < 10:
            errors['edit_description'] = "Description should be at least 10 characters"
        if len(postData['edit_location']) < 1:
            errors['edit_location'] = "Location should not be left blank"
        return errors

class Job(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    poster = models.ForeignKey(User,related_name='poster', on_delete = models.CASCADE)
    my_job = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    objects = JobManager()