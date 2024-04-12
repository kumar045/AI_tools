from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.TextConversion.as_view(), name="Text_Conversion"),
    path('file/', views.FileConversion.as_view(), name="File_Conversion"),
    path('pdf2pdf/', views.PdfFileConversion.as_view(), name="Pdf_File_Conversion"),
    
]
