from django.db import models


class TextModel(models.Model):
    
    data = models.TextField() 
    targetLanguage = models.CharField(max_length=255)
    targetLanguageCode = models.CharField(max_length=255)
    
    


class FileModel(models.Model):
    
    file = models.FileField(upload_to="uploads/")
    targetLanguage = models.CharField(max_length=255)
    