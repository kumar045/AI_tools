from django.db import models


class TextModel(models.Model):
    
    data = models.TextField()
    sourceLanguageCode = models.CharField(max_length=255) 
    targetLanguage = models.CharField(max_length=255)
    targetLanguageCode = models.CharField(max_length=255)
    
    


class FileModel(models.Model):
    
    file = models.FileField(upload_to="uploads/")
    targetLanguage = models.CharField(max_length=255)

    

class PdfFileModel(models.Model):
    
    file = models.FileField(upload_to="uploads/")
    targetLanguage = models.CharField(max_length=255)
    sourceLanguage = models.CharField(max_length=255)
    
    
