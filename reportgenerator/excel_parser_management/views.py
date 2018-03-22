# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import pdb
import json
import pandas as pd
import numpy as np
import xlsxwriter
import re
import json
from datetime import datetime
import threading

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser,MultiPartParser


from .serializers import (
	ExcelExtractedDataSerializer,
	ExcelJobSerializer,
	ExcelExtractedDataMongoSerializer
	)

from .models import (
	ExcelExtractedDataMongo,
	ExcelJobs
	)

from masters.models import(
	AccountNames
	)
# Create your views here.


class JobList(ListAPIView):
	"""this class is used to list the jobs"""
	queryset = ExcelJobs.objects.all()
	serializer_class = ExcelJobSerializer

class ExcelManagementList(APIView):

	"""this class is used to filter the data from mongo db 2541-769830 08/11/2017 08:19:00"""
	
	def post(self,request):
		

		filter_item = request.data
		excelextracted_obj = ExcelExtractedDataMongo.objects

		if filter_item['job_id']:
			excelextracted_obj = excelextracted_obj.filter(job_id = filter_item['job_id'] )

		if filter_item['account_name']:
			excelextracted_obj = excelextracted_obj.filter(account_name = filter_item['account_name'] )

		if filter_item['asset_id']:
			excelextracted_obj = excelextracted_obj.filter(asset_location__startswith = filter_item['asset_id'] )

		if filter_item['department_name']:
			excelextracted_obj = excelextracted_obj.filter(department_name = filter_item['department_name'] )

		if filter_item['failure_reason_id']:
			excelextracted_obj = excelextracted_obj.filter(failure_reason_id = filter_item['failure_reason_id'] )

		if filter_item['closed']['start_time']:
			#filter_date = datetime.strptime(filter_item['closed'], "" )
			start_time = datetime.strptime(filter_item['closed']['start_time'], "%Y-%m-%d").isoformat()
			end_time = datetime.strptime(filter_item['closed']['end_time'], "%Y-%m-%d").isoformat()
			excelextracted_obj = excelextracted_obj.filter( \
				closed__gte = start_time, \
				closed__lte = end_time \
				 )
		return Response({"data":excelextracted_obj.to_json()})

	

class ExcelManagementUpload(APIView):

	"""this class is used to upload file, create a job and process the job"""

	parser_classes = (MultiPartParser,)


	def process_excel_file(self,job_id):
		COMPLETED,ERROR = 2,3
		job_instance = ExcelJobs.objects.get(id = job_id)
		job_id = job_id
		job_document = job_instance.document.url

		colomn_name_dict = { 
			"Asset / Location":  "asset_location",
			"Closed":  "closed",
			"Labor Report":  "labor_report",
			"Department Name":  "department_name",
			"Target Date":  "target_date",
			"Account Name":  "account_name",
			"Failure Reason Name":  "failure_reason_name",
			"Failure Reason ID":"failure_reason_id",
			"Model":  "model", 
			"Asset Name":  "asset_name",
			"Manufacturer Name":  "manufacturer_name",
			"Work Order #":  "work_order", 
			"Reason":  "reason"
		}

		xl = pd.ExcelFile('./'+job_document)
		sheet_name = xl.sheet_names[0]
		df = xl.parse(sheet_name)
		df.rename(columns=colomn_name_dict, inplace=True)
		
		excel_json_data =  json.loads(df.reset_index().to_json(orient='records'))

		data_time_now = datetime.now()
		pre_documents = []

		for data in excel_json_data:
			print data
			pre_documents.append(
				ExcelExtractedDataMongo( \
							job_id 					= job_id, \
							account_name 			= data['account_name'], \
							asset_location 			= data['asset_location'], \
							asset_name 				= data['asset_name'], \
							model 					= data['model'], \
							manufacturer_name 		= data['manufacturer_name'], \
							failure_reason_id 		= data['failure_reason_id'], \
							reason 					= data['reason'], \
							work_order 				= data['work_order'], \
							failure_reason_name 	= data['failure_reason_name'], \
							department_name 		= data['department_name'], \
							labor_report 			= data['labor_report'], \
							closed 					= datetime.fromtimestamp(data['closed']/1000.0), \
							target_date 			= datetime.fromtimestamp(data['target_date']/1000.0), \
							created_on 				= data_time_now, \
							updated_on 				= data_time_now, \
							created_by 				= 1, \
							updated_by				= 1
							)
				)

			# AccountNames.objects.get_or_create( \
			# 	account_name = strip(data['account_name'])\
			# 	)
							
		ExcelExtractedDataMongo.objects.insert(pre_documents)
		job_instance.status = COMPLETED
		print "completed"
		job_instance.save()

	def post(self,request,*args, **kwargs):
		
		job_instance = ExcelJobSerializer(data=request.data)
		if job_instance.is_valid():
			job_instance.save()
			thread = threading.Thread(target=self.process_excel_file, \
				args=(job_instance.data['id'],))
			thread.start()
			
		return Response({"status":"success"})

