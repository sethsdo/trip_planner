from __future__ import unicode_literals
import re
from django.db import models
import datetime


emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class userManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        print postData
        for input in postData:
            if len(postData[input]) < 2:
                errors['input'] = "All fields are required"
            # elif not postData['name'].isalpha():
            #     errors['name'] = "Invalid  name!"
            elif not postData['username'].isalpha():
                errors['username'] = "Invalid  username!"
            elif postData['password'] < 8:
                errors['password'] = "Invalid password..."
            elif postData['password'] != postData['confirm_password']:
                errors['confirm_password'] = "Passwords dont match!"
            return errors

    def login_validator(self, postData):
        errors = {}
        for input in postData:
            if len(postData[input]) < 3:
                errors['input'] = "All fields are required"
            elif postData['password'] < 8:
                errors['password'] = "Invalid password..."
            return errors

    def trip_validator(self, postData):
        errors = {}
        for input in postData:
            if len(postData[input]) < 3:
                errors['input'] = "Trip not applied, All fields are required"
            return errors


class user(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = userManager()

    def __repr__(self):
        return "<user object: {} {}>".format(self.name, self.username)

class trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    start = models.TextField()
    end = models.TextField()
    creator = models.ForeignKey(user, related_name="trip_id", null=True)
    users = models.ManyToManyField(user, related_name="trips")

    objects = userManager()

    def __repr__(self):
        return "<trip object: {} {} {} {} {}>".format(self.destination, self.plan, self.start, self.end, self.users)
