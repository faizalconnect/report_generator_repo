from rest_framework import serializers
from .models import (
	ExcelExtractedData,
	ExcelJobs,
	ExcelExtractedDataMongo
	)
from rest_framework_mongoengine.serializers import DocumentSerializer

class ExcelExtractedDataMongoSerializer(DocumentSerializer):
	"""serializer for inserting data to monogp dataase"""
	class Meta:
		model = ExcelExtractedDataMongo
		#depth = 2
		fields = ('job_id','account_name', 'asset_location', 'asset_name', \
		 		  'closed', 'department_name', 'failure_reason_id' \
		 		  ,'failure_reason_name','labor_report','manufacturer_name', \
		 		  'model','reason','target_date','work_order',\
		 		  'created_on','created_by','updated_on','updated_by')




class ExcelExtractedDataSerializer(serializers.ModelSerializer):
	
	#"""This serializer is used to serialize data got from ExcelExtractedData table"""
    
    class Meta:
        model = ExcelExtractedData
        fields = ('account_name', 'asset_location', 'asset_name', \
         		  'closed', 'department_name', 'failure_reason_id' \
         		  ,'failure_reason_name','labor_report','manufacturer_name', \
         		  'model','reason','target_date','work_order')


class ExcelJobSerializer(serializers.ModelSerializer):
	#document = serializers.FileField(max_length=None,use_url=True)
	class Meta:
		model = ExcelJobs
		fields = ('id', 'job_name', 'document', 'status', 'created_on')