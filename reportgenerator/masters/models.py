# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class AccountNames(models.Model):
	"""model for keeping account name"""
	account_name =  models.CharField(max_length = 255,blank=True, null=True)

	def __str__(self):
		return str(self.pk) +" : "+ str(self.account_name)	

class Manufacture(models.Model):
	"""model for keeping manufacture name"""
	manufacturer_name	=  models.CharField(max_length = 100,blank=True, null=True)	
	
	def __str__(self):
		return str(self.pk) +" : "+ str(self.manufacturer_name)

class Assets(models.Model):
	"""model for keeping assets informations"""
	asset_name 			=  models.CharField(max_length = 255,blank=True, null=True)
	model  				=  models.CharField(max_length = 100,blank=True, null=True)
	manufacture         =  models.ForeignKey(Manufacture, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.pk) +" : "+ str(self.asset_name)
	
class Departments(models.Model):
	"""model for keeping departments name"""
	department_name			=  models.CharField(max_length = 100,blank=True, null=True)

	def __str__(self):
		return str(self.pk) +" : "+ str(self.department_name)			

class FailureReason(models.Model):
	"""model for keeping failure reason"""
	failure_reason_id 		= models.CharField(max_length = 20,blank=True, null=True)
	failure_reason 			= models.CharField(max_length = 255,blank=True, null=True)
	asset 					= models.ForeignKey(Assets, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.pk) \
			+" : "+ str(self.failure_reason_id) \
			+" : "+ str(self.failure_reason)		
