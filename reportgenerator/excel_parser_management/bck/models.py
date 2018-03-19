# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import *
from django.db import models

# Create your models here.
class ExcelExtractedData(models.Model):
	
	#"""This model is used to keep extracted data from the excel file These are the fields listed in excel file"""

		account_name 		= models.TextField(blank=True, null=True)
		asset_location 		= models.TextField(blank=True, null=True)
		asset_name 			= models.TextField(blank=True, null=True)
		closed 				= models.TextField(blank=True, null=True)
		department_name 	= models.TextField(blank=True, null=True)
		failure_reason_id 	= models.TextField(blank=True, null=True)
		failure_reason_name = models.TextField(blank=True, null=True)
		labor_report 		= models.TextField(blank=True, null=True)
		manufacturer_name 	= models.TextField(blank=True, null=True)
		model 				= models.TextField(blank=True, null=True)
		reason 				= models.TextField(blank=True, null=True)
		target_date 		= models.TextField(blank=True, null=True)
		work_order 			= models.TextField(blank=True, null=True)


		def __str__(self):
			return str(self.account_name)


class ExcelExtractedDataMongo(Document):
	job_id = IntField(required = True)
	data = DictField(required=True)
	

class ExcelJobs(models.Model):
	"""Table for adding new jobs"""

	STATUS_CHOICES = (
		(1,"IN PROGRESS"),
		(2,"COMPLETED"),
		(3,"ERROR")
		)
	
	job_name = models.CharField(max_length=50,blank=True,null=True)
	document = models.FileField(upload_to='documents/')
	status   = models.IntegerField(choices=STATUS_CHOICES, default=1)
	created_on = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
			return str(self.pk) + " "+str(self.job_name)
		

	
		