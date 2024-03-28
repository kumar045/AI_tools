from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .languageCodes import getLanguageCode
import torch
from . import serializers
from . import utilsFile
import logging






class TextConversion(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Get Request Not Allowed"
            } 
        )
    def post(self, request, *args, **kwargs):
        
        # Accepting Values
        try:
           data = request.data['text']
           targetLanguage = request.data['targetLanguage']
         
        except Exception as e:
           return Response(
               {
                   'status':status.HTTP_400_BAD_REQUEST,
                   "response":"Key Error, Key required, 'text' and 'targetLanguage'"
               }
           )
        
        # Getting Target Language Code
        try:
            targetLanguageCode = getLanguageCode(targetLanguage)
        
        except Exception as e:
            return Response(
               {
                   'status':status.HTTP_404_NOT_FOUND,
                   "response":"Target Language is not Allowed"
               }
           )
        
        collectedData = {
            "data":data,
            "targetLanguage":targetLanguage,
            "targetLanguageCode":targetLanguageCode
        }

  
       
        # Serializing input
        serializer = serializers.TextModelSerializer(data=collectedData)
        if serializer.is_valid():     
   
            response = utilsFile.textView(serializer.data['data']+". ", serializer.data['targetLanguageCode'])
            
            return Response(
                {
                    'status':status.HTTP_200_OK,
                    'response':response
                }
            )
        return Response(
        {
            'status':status.HTTP_400_BAD_REQUEST,
            'response':str(serializer.errors)
        }
    )  
    def put(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Put Request Not Allowed"
            } 
        )
    def patch(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Patch Request Not Allowed"
            } 
        )
    def delete(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Delete Request Not Allowed"
            } 
        )
    

    

class FileConversion(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Get Request Not Allowed"
            } 
        )
    def post(self, request, *args, **kwargs):
        
        # Accepting Values
        try:
           file = request.data['file']
           targetLanguage = request.data['targetLanguage']
        except Exception as e:
           return Response(
               {
                   'status':status.HTTP_400_BAD_REQUEST,
                   "response":"Key Error, Key Required, 'file' and 'targetLanguage'"
               }
           )
        
        # Getting Target Language Code
        try:
            targetLanguageCode = getLanguageCode(targetLanguage)

        except Exception as e:
            return Response(
               {
                   'status':status.HTTP_404_NOT_FOUND,
                   "response":"Given Target Language is not Allowed"
               }
           )
        
        
        # 1. Get and Store file in temprory directory
        serializer = serializers.FileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                {
                    'status':status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'response':"Invalid File Serializer is not able to serialize."
                }
            )
        
        
        
        # 2. Extract Text From the File
        convertedResponse = utilsFile.fileView(
            filePath=serializer.data['file'],
            targetLanguageCode=targetLanguageCode
        )

        
        
        return Response(
            {
                'status':status.HTTP_200_OK,
                'response':convertedResponse
            }
        )
    def put(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Put Request Not Allowed"
            } 
        )
    def patch(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Patch Request Not Allowed"
            } 
        )
    def delete(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Delete Request Not Allowed"
            } 
        )
    