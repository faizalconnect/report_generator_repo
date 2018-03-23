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
import logging



from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework import serializers 

#from reportgenerator.core.constants import *
from rest_framework import status

from excel_parser_management.serializers import (
	ExcelExtractedDataSerializer,
	ExcelJobSerializer,
	ExcelExtractedDataMongoSerializer
	)

from excel_parser_management.models import (
	ExcelExtractedDataMongo,
	ExcelJobs
	)

from masters.models import(
	AccountNames
	)


# Create your views here.

logger = logging.getLogger(__name__)
class JobList(ListAPIView):
	"""this class is used to list the jobs"""
	queryset = ExcelJobs.objects.all()
	serializer_class = ExcelJobSerializer


class ExcelManagementList(APIView):

	"""this class is used to filter the data from mongo db"""
	
	# @use : this function is used to filter the data from mongo db
	# @params: {"job_id" => id of the job,"account_name","asset_id","department_name",
	#			,"failure_reason_id","closed"}
	# @return: void
	def post(self,request):
		

		filter_item = request.data
		excelextracted_obj = ExcelExtractedDataMongo.objects

		#filtering the mongodb data wrt job id
		if filter_item['job_id']:
			excelextracted_obj = excelextracted_obj.filter(job_id = filter_item['job_id'] )

		#filtering the mongodb data wrt account name
		if filter_item['account_name']:
			excelextracted_obj = excelextracted_obj.filter(account_name = filter_item['account_name'] )

		#filtering the mongodb data wrt asset id	
		if filter_item['asset_id']:
			excelextracted_obj = excelextracted_obj.filter(asset_location__startswith = filter_item['asset_id'] )

		#filtering the mongodb data wrt department name	
		if filter_item['department_name']:
			excelextracted_obj = excelextracted_obj.filter(department_name = filter_item['department_name'] )

		#filtering the mongodb data wrt failure reason
		if filter_item['failure_reason_id']:
			excelextracted_obj = excelextracted_obj.filter(failure_reason_id = filter_item['failure_reason_id'] )

		#filtering the mongodb data wrt close time
		if filter_item['closed']['start_time']:
			#filter_date = datetime.strptime(filter_item['closed'], "" )
			start_time = datetime.strptime(filter_item['closed']['start_time'], "%Y-%m-%d").isoformat()
			end_time = datetime.strptime(filter_item['closed']['end_time'], "%Y-%m-%d").isoformat()
			excelextracted_obj = excelextracted_obj.filter( \
				closed__gte = start_time, \
				closed__lte = end_time \
				 )
		#serialising the filterd data	
		serialized = ExcelExtractedDataMongoSerializer(excelextracted_obj, many = True)
		return Response(serialized.data)

	

class ExcelManagementUpload(APIView):

	"""this class is used to upload file, create a job and process the job"""

	parser_classes = (MultiPartParser,)

	# @use : this function is used to process the uploaded excel file
	# @params: {"job_id" => id of the job}
	# @return: void
	def process_excel_file(self,job_id):
		try:

			#status code
			COMPLETED,ERROR = 2,3
			#get the job details wrt job id
			job_instance = ExcelJobs.objects.get(id = job_id)
			#get the document url
			job_document = job_instance.document.url

			#formating the header of the uploaded document
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

			#opening the uploaded excel file
			xl = pd.ExcelFile('./'+job_document)
			#reading the first sheet of the excel file
			sheet_name = xl.sheet_names[0]
			df = xl.parse(sheet_name)
			df.rename(columns=colomn_name_dict, inplace=True)
			
			excel_json_data =  json.loads(df.reset_index().to_json(orient='records'))

			data_time_now = datetime.now()
			pre_documents = []

			#extracting each rows of the excel file to instaert into mongodb
			for data in excel_json_data:
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

			#inserting the excel file into mongo db collection ExcelExtractedDataMongos 					
			ExcelExtractedDataMongo.objects.insert(pre_documents)
			job_instance.status = COMPLETED
			job_instance.save()
			logging.debug("jobid:%s, file processing completed  "%(str(job_instance.id)))
		
		except Exception as ex:
			logging.debug("jobid:%s,%s  "%(str(job_instance.id),str(ex)))


	# @use : this function is used to create a job upload excel file
	# @params: 
	# @return: {"success" or "failed"}
	def post(self,request,*args, **kwargs):
		result = {}
		result['status'] = True
		result['message'] = "file uploaded successfully"
		result['errormsg'] = ""
		RESPONSE_STATUS = status.HTTP_200_OK

		try:

			#parsing the posted data 
			job_instance = ExcelJobSerializer(data=request.data)
			#validating the data
			if job_instance.is_valid():
				#saving a job
				job_instance.save()

				jobid = job_instance.data['id']
				#processing the uploaded filed on thread
				thread = threading.Thread(target=self.process_excel_file, \
					args=(jobid,))
				thread.start()
				logging.info("jobid:%s, file uploaded success fully"%(str(jobid)))
			else:
				
				RESPONSE_STATUS = status.HTTP_400_BAD_REQUEST
				result['status'] = False
				result['message'] = "file uploading failed"
				result['errormsg'] =  job_instance.errors
				logging.debug(str(job_instance.errors))

		except Exception as ex:
			RESPONSE_STATUS = status.HTTP_403_FORBIDDEN
			result['status'] = False
			result['message'] = "file uploading failed"
			result['errormsg'] = str(ex)
			logging.debug(str(ex))
			
		return Response(result,status=RESPONSE_STATUS)



