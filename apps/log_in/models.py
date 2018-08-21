from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
import bcrypt
from datetime import datetime, time, date
from time import strftime


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        result={}
        errors =[]

        if len(postData['first_name']) <2:
            errors.append("Frist name should be at least 2 characters")
        elif not postData['first_name'].isalpha():
            errors.append("Frist name must be letters only")
        if len(postData['last_name']) <2:
            errors.append("Last name should be at least 2 characters")
        elif not postData['last_name'].isalpha():
            errors.append("last name must be letters only")
        # if User.objects.filter(email = postData['email']):
        #     errors.append("This Email already exists!")
        if len(postData['email']) <1: 
            errors.append("Email cannot be empty")
        else: 
            try:
                validate_email(postData['email'])
            except:
                errors.append("Not a valid email")
        if len(postData['password'])<1:
            errors.append("Password cannot be empty")
        elif len(postData['password'])<8:
            errors.append("Password require at least 8 characters")
        if len(postData['confirm_password'])<1:
            errors.append("Confirm password cannot be empty")
        if postData['password'] != postData['confirm_password']:
            errors.append("Password doesn't match")
        if len(errors) == 0:
            # bcrypt hashing password
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user_hash = hash1.decode('utf8') 
            
            new_user = User.objects.create(
                first_name = postData['first_name'],
                last_name = postData['last_name'],
                email = postData['email'],
                password = new_user_hash 
            )
            result['user_id'] = new_user.id
            print('------------new user generated-------------')
        else:
            result['errors'] = errors
        return result

    def login_validator(self,postData):
        checkfor_user = User.objects.filter(email=postData['email'])
        result = {
            'user_status' : False,
            'errors' : []
        }
        if len(postData['email']) <1: 
            result['errors'].append("Email cannot be empty")
            return result
        else: 
            try:
                validate_email(postData['email'])
            except:
                result['errors'].append("Not a valid email format")
                return result
        if checkfor_user.count() == 0:
            result['errors'].append("Invalid login information")
        else:
            if bcrypt.checkpw(postData['password'].encode(), checkfor_user[0].password.encode()):
                result['user_status'] = True
                result['user_id'] = checkfor_user[0].id
                print('i am checking password')
            else:
                result['errors'].append("Log in failed")
        print(result)
        return result


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {}>".format(self.first_name, self.last_name , self.email)

class JobManager(models.Manager):
    def job_validator(self, postData,user_id):
        result={}
        errors =[]
        if len(postData['title']) < 1:
            errors.append('Job title cannot be empty')
        elif len(postData['title']) <3:
            errors.append("Title should be at least 3 characters")
        if len(postData['desc']) < 1:
            errors.append('Job description cannot be empty')
        elif len(postData['desc']) <10:
            errors.append("Job description should be at least 10 characters")
        if len(postData['location']) < 1:
            errors.append("location must not be blank")
        if len(errors) == 0:
            me = User.objects.get(id=user_id)
            new_job = Job.objects.create(
                title = postData['title'],
                desc = postData['desc'],
                location = postData['location'],
                created_by = me
            )
            print('------------new Job created -------------')
        else:
            result['errors'] = errors    

        return result
    def editjob_validator(self, postData):

        result={}
        errors =[]
        if len(postData['title']) < 1:
            errors.append('Job title cannot be empty')
        elif len(postData['title']) <3:
            errors.append("Title should be at least 3 characters")
        if len(postData['desc']) < 1:
            errors.append('Job description cannot be empty')
        elif len(postData['desc']) <10:
            errors.append("Job description should be at least 10 characters")
        if len(postData['location']) < 1:
            errors.append("location must not be blank")
        if len(errors) == 0:
            print('errors is', errors)
            return result   
        else:
            result['errors']=errors
            return result

class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name = 'cancreate_jobs', on_delete = models.CASCADE)
    taken_by = models.ForeignKey(User, related_name ='cantake_jobs',on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
    def __repr__(self):
        return f"<Item Object {self.title} {self.desc}>"