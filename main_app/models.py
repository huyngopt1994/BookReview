from __future__ import unicode_literals

from django.db import models

import bcrypt
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

NAME_REGEX = re.compile(r'^[A-Za-z]+\s?[a-zA-z]+$') # because your name should start from a character
# \w can include alphanumeric character, underscore as well.
# Create your models here.

class UserManager(models.Manager):
	def validate_register(self, post_data):
		"""

		:param post_data: a dict which contain data of registeration
		:return: list error ( if it's good it should be an empty list)
		"""
		errors = []

		# check the len of fields :
		if len(post_data['name']) <3 or len(post_data['alias']) <1:
			errors.append('name should be larger than 3, alias should be larger than 1')
		if len(post_data['password']) <8:
			errors.append('password must be at least 8 characters')
		if (not re.match(NAME_REGEX, post_data['name']) or not re.match(NAME_REGEX, post_data['alias'])):
			errors.append('your name should contain only alpha characters')
		if (not re.match(EMAIL_REGEX, post_data['email'])):
			errors.append('email is invalid')
		# verifi the email was used or not
		if len(User.objects.filter(email=post_data['email'])) >0:
			errors.append('email was used')
		# verify the confirm_password and password
		if  post_data['confirm_password'] != post_data['password']:
			errors.append('confirm_password doesn"t match with password')

		return errors

	def validate_login(self, post_data):
		"""
		:param post_data: a dict which contain of login
		:return: list error ( if it's good it should be an empty list)
		"""
		errors = []
		# steps to verify login phase :
		# 1./ verify email existed
		# 2./ hashing the passed password and compare with stored password

		# Check DB if email existed or not
		users = self.filter(email=post_data['email'])
		if len(users) >0:
			# yep we got this user, so right now we will check this password

			if not bcrypt.checkpw(post_data['password'].encode(), users[0].password.encode()):
				errors.append('password is incorrect')
		else:
			errors.append('email is incorrect')
		return errors


class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	objects = UserManager()


class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	poster = models.ForeignKey(User, related_name="uploaded_books")
	created_at = models.DateTimeField(auto_now_add=True)


# Create a middle table to handle many to many relationship
class Review(models.Model):
	rating = models.IntegerField(default=0)
	content = models.TextField()
	reviewer = models.ForeignKey('User', related_name="reviews_left")
	book = models.ForeignKey('Book', related_name="reviews")
	created_at = models.DateTimeField(auto_now_add=True)
