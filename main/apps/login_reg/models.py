from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#import libraries re and bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate(self, form):
        errors = []
        #validate the form
        if len(form['first_name']) <2:
            errors.append('First name must be longer than 2 characters.')
        if len(form['last_name']) <2:
            errors.append('Last name must be longer than 2 characters.')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Email must be valid.')
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters long.')
        if form['password'] != form['confirm_pw']:
            errors.append('Passwords much match.')

#if validation passes. now check to see if email is in the db.
        if self.filter(email=form['email']):
            errors.append('Email already in use.')
#if we find errors return them to the function that called in in the views file.
        return errors

    def create_user(self, form_data):
        pw_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
        return self.create(
            first_name = form_data['first_name'],
            last_name =form_data['last_name'],
            email = form_data['email'],
            pw_hash = pw_hash,

        )

    def login_user(self, form_data):
        user_list = User.objects.filter(email=form_data['email'])
        if len(user_list) > 0 :
            print(user_list)
            user = user_list[0]
            if bcrypt.checkpw(form_data['password'].encode(), user.pw_hash.encode()):
                return(True, user.id)
            else:
                return(False, "Email or passwords don't match.")
        else:
            return (False, "Email or passwords don't match.")


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.email
