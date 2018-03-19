# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import pdb
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser,MultiPartParser


from .serializers import (
	ExcelExtractedDataSerializer,
	ExcelJobSerializer,
	#ExcelExtractedDataMongoSerializer
	)

from .models import (
	ExcelExtractedDataMongo
	)
# Create your views here.

class ExcelManagement(APIView):


	"""docstring for User"""
	
	parser_classes = (MultiPartParser,)
	def get(self,request):

		# {
		#     "a": "value of a",
		#     "somedict": {
		#         "someinfo": [
		#             {
		#                 "name": "Jordan",
		#                 "food": [
		#                     "fries",
		#                     "coke",
		#                     "drink"
		#                 ]
		#             }
		#         ]
		#     }
		# }
		# 1) "name='Jordan'"  Sample.objects(somedict__someinfo__name='Jordan')
		# 2)'food' contains 'fries'? Sample.objects(somedict__someinfo__food='Fries')
		# ExcelExtractedDataMongo.objects.filter(data__target_date = 1511222400000 )

		#excel_json_data = [{"0":{"account_name":"Bellevue Hospital Center","asset_location":"2541-631991","asset_name":"Scanning Systems, Computed Tomography, Axial, Full-Body","model":"LightSpeed VCT","manufacturer_name":"General Electric Med. Systems","failure_reason_id":"F3","reason":"CAT-SCAN WILL NOT SCAN","work_order":"2541-769830","failure_reason_name":"Equipment Failure, Total (Sys down -same day RPR)","department_name":"Cat Scan","labor_report":"Checked machine found was not coming on. Troubleshoot system found Auxiliary Box was not working %0D%0Aproperly. Replaced Aux Box. Performed a function test, Tube warmup and Fast Calibrations. All %0D%0Afunctions tested ok. Turned system back into service for clinical use.","target_date":1511222400000,"closed":1511332620000},"1":{"account_name":"Bellevue Hospital Center","asset_location":"2541-644217","asset_name":"Radiographic Unit","model":451220102551,"manufacturer_name":"PHILIPS MEDICAL SYSTEMS, INC","failure_reason_id":"F1","reason":"UPRIGHT TRACK DOES NOT MOVE PROPERLY WITH BUCKY","work_order":"2541-764271","failure_reason_name":"Equipment Failure, Minor","department_name":"Er Trauma","labor_report":"Checked machine found wall bucky tilt encoder gear had some broken teeth. Moved %0D%0Agear to a different position, reset the auto tracking. Performed a function test and all %0D%0Atested ok.","target_date":1509667200000,"closed":1509695040000}}
		excel_json_data = [{"index":0,"account_name":"Bellevue Hospital Center","asset_location":"2541-631991","asset_name":"Scanning Systems, Computed Tomography, Axial, Full-Body","model":"LightSpeed VCT","manufacturer_name":"General Electric Med. Systems","failure_reason_id":"F3","reason":"CAT-SCAN WILL NOT SCAN","work_order":"2541-769830","failure_reason_name":"Equipment Failure, Total (Sys down -same day RPR)","department_name":"Cat Scan","labor_report":"Checked machine found was not coming on. Troubleshoot system found Auxiliary Box was not working %0D%0Aproperly. Replaced Aux Box. Performed a function test, Tube warmup and Fast Calibrations. All %0D%0Afunctions tested ok. Turned system back into service for clinical use.","target_date":1511222400000,"closed":1511332620000},{"index":1,"account_name":"Bellevue Hospital Center","asset_location":"2541-644217","asset_name":"Radiographic Unit","model":451220102551,"manufacturer_name":"PHILIPS MEDICAL SYSTEMS, INC","failure_reason_id":"F1","reason":"UPRIGHT TRACK DOES NOT MOVE PROPERLY WITH BUCKY","work_order":"2541-764271","failure_reason_name":"Equipment Failure, Minor","department_name":"Er Trauma","labor_report":"Checked machine found wall bucky tilt encoder gear had some broken teeth. Moved %0D%0Agear to a different position, reset the auto tracking. Performed a function test and all %0D%0Atested ok.","target_date":1509667200000,"closed":1509695040000}]
		# instance = ExcelExtractedDataSerializer(data = excel_json_data, many = True)
		# if instance.is_valid():
		# 	instance.save()

		#saving the data
		pdb.set_trace()
		# for data in excel_json_data:
		# 	instance = ExcelExtractedDataMongo()
		# 	instance.job_id = 1
		# 	instance.data = data
		# 	instance.save()

		pdb.set_trace()

		#listing the data
		



		return Response({"data":ExcelExtractedDataMongo.objects.to_mongo()})

	def post(self,request,*args, **kwargs):
		
		print request.FILES
		instance = ExcelJobSerializer(data=request.data)
		pdb.set_trace()
		if instance.is_valid():
			pdb.set_trace()
			instance.save()
		return Response({"data":"data"})

