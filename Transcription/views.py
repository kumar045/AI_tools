from rest_framework.views import APIView
from .serializers import *
from Transcription.utils.app import transcript
from rest_framework.response import Response

class TranscriptionView(APIView):
    @staticmethod
    def post(request):
        payload = TranscriptionSerializer(data=request.data)
        if payload.is_valid(raise_exception=True):
            query_file = payload.validated_data.get('file')
            file_path = "query.wav"
            # Saving the file to the disk
            with open(file_path, 'wb+') as destination:
                for chunk in query_file.chunks():
                    destination.write(chunk)
            transcription = transcript(file_path)
            return Response(status=200, data={"transcription": transcription})
        else:
            return Response(status=400, data={"message": "Invalid data"})