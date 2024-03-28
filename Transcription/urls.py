
from django.urls import path

from .views import *

urlpatterns = [
    path("transcription", TranscriptionView.as_view(), name="get_transcription"),
]