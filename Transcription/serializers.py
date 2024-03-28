from rest_framework import serializers

class TranscriptionSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)