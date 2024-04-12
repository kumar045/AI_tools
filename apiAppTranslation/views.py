from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .languageCodes import getLanguageCode
import torch
from . import serializers
from . import utilsFile, pdfTranslate
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
           sourceLanguage = request.data['sourceLanguage']
           targetLanguage = request.data['targetLanguage']
         
        except Exception as e:
           return Response(
               {
                   'status':status.HTTP_400_BAD_REQUEST,
                   "response":"Key Error, Key required, 'text', 'sourceLanguage' and 'targetLanguage'"
               }
           )
        
        # Getting Target Language Code
        try:
            print(targetLanguage)
            targetLanguageCode = getLanguageCode(targetLanguage)

            if sourceLanguage.lower() != "auto":
                sourceLanguageCode = getLanguageCode(sourceLanguage)
            else:
                sourceLanguageCode = "auto"
                
        except Exception as e:
            return Response(
               {
                   'status':status.HTTP_404_NOT_FOUND,
                   "response":"Target or Source Language is not Allowed"
               }
           )
        
        collectedData = {
            "data":data,
            "sourceLanguageCode":sourceLanguageCode,
            "targetLanguage":targetLanguage,
            "targetLanguageCode":targetLanguageCode
        }

        # Serializing input
        serializer = serializers.TextModelSerializer(data=collectedData)
        if serializer.is_valid():     
   
            response = utilsFile.textView(
                myStr=serializer.data['data']+". ", 
                targetLanguageCode=serializer.data['targetLanguageCode'],
                sourceLanguageCode=sourceLanguageCode)
            
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
           sourceLanguage = request.data['sourceLanguage']
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
            if sourceLanguage.lower() != "auto":
                sourceLanguageCode = getLanguageCode(sourceLanguage)
            else:
                sourceLanguageCode = sourceLanguage

        except Exception as e:
            return Response(
               {
                   'status':status.HTTP_404_NOT_FOUND,
                   "response":"Given Target Language Or Source Language is not Allowed"
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
        
        
        if serializer.data['file'].split(".")[-1] not in ['docx','pdf','txt']:
             return Response(
                {
                    'status':status.HTTP_400_BAD_REQUEST,
                    'response':"File Type Not Allowed"
                }
            )
        else:
            # 2. Extract Text From the File
            convertedResponse = utilsFile.fileView(
                filePath=serializer.data['file'],
                targetLanguageCode=targetLanguageCode,
                sourceLanguageCode=sourceLanguageCode
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
    
class PdfFileConversion(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                "response":"Get Request Not Allowed"
            } 
        )
    def post(self, request, *args, **kwargs):
        print(request.data)
        
        # Accepting Values
        try:
           file = request.data['file']
           targetLanguage = request.data['targetLanguage']
           sourceLanguage = request.data['sourceLanguage']
        except Exception as e:
           print(str(e))
           return Response(
               {
                   'status':status.HTTP_400_BAD_REQUEST,
                   "response":"Key Error, Key Required, 'file' 'sourceLanguage' and 'targetLanguage'"
               }
           )
        
        # Getting Target Language Code
        try:
            targetLanguageCode = getLanguageCode(targetLanguage)
            
            if sourceLanguage.lower() != "auto":
                sourceLanguageCode = getLanguageCode(sourceLanguage)
            else:
                sourceLanguageCode = "auto"

        except Exception as e:
            return Response(
               {
                   'status':status.HTTP_404_NOT_FOUND,
                   "response":"Given Target Language is not Allowed"
               }
           )
        
        
        # 1. Get and Store file in temprory directory
        serializer = serializers.PdfFileModelSerializer(data=request.data)
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
        convertedResponse = pdfTranslate.fileView(
            filePath=serializer.data['file'],
            targetLanguageCode=targetLanguageCode,
            sourceLanguageCode=sourceLanguageCode
        )

        
        
        return Response(
            {
                'status':status.HTTP_200_OK,
                "isPdf":True,
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
    
