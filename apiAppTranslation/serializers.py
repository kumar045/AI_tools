from rest_framework import serializers
from . import models

class TextModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.TextModel
        fields = "__all__"
    
    

class FileModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FileModel
        fields = "__all__"
    
    def get_file_name(self, instance):
        return instance.file.name.split("/")[-1]