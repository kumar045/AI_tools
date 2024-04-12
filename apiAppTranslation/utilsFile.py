import torch
from rest_framework.response import Response
from rest_framework import status
from .mlModel.M2M100_bert import loadModelLanguageConversion
from .mlModel.Seamless_m4t_v2_large import translator
from django.core.files.uploadedfile import InMemoryUploadedFile
from PyPDF2 import PdfReader
from . import languageCodes
import easyocr
from pdf2image.pdf2image import convert_from_path
import pytesseract
import io
import re
from django.conf import settings   
import docx2txt 
import os
from .languageCodes import getLanguageCode2To3
from ftlangdetect import detect



def checkLanguage(sourceText=""):
    '''
        This Function is using XLM_Roberta for language detection
        Paramers:
            sourceText : string
    '''
    try:
        detected_language = detect(text=sourceText, low_memory=False)
    
        return getLanguageCode2To3(languageCode=detected_language["lang"])
    except:
        return "eng"
    

def makePrediction(
    sourceTextList=[""], 
    sourceLanguageCode="",
    targetLanguageCode=""
    ):
    '''
        This Function will make prediction, following parameter is required
        
        SourceTextList: str,
        SourceLanguageCode: str,
        targetLanguageCode: str
    '''
    # Uncomment for M2M100_bert.py
    # tokenizerLanguageConversion.src_language = sourceLanguageCode
    
    translatedText = ""
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    for sourceText in sourceTextList:
        
        # Commented code will work on M2M100_bert.py Model
        # ------------------------------------------------------------------------
        # with torch.no_grad():
        #     encoded_input = tokenizerLanguageConversion(sourceText, return_tensors="pt").to(device)
        #     generated_tokens = modelLanguageConversion.generate(
        #         **encoded_input, forced_bos_token_id=tokenizerLanguageConversion.get_lang_id(targetLanguageCode)
        #     )
           
        #     translated_text = tokenizerLanguageConversion.batch_decode(
        #         generated_tokens, skip_special_tokens=True
        #     )[0]
            
        #     translatedText += translated_text
        # -------------------------------------------------------------------------
        outputText = translator.predict(
            input=sourceText,
            task_str="T2TT",
            tgt_lang=targetLanguageCode,
            src_lang=sourceLanguageCode,
            text_generation_opts=None,
            unit_generation_opts=None
        )
        
    
         # Using regular expression to extract text within single quotes
        translated_text = re.search(r"'(.*?)'", str(outputText[0])).group(1)
        translatedText += translated_text.replace("We need to make sure that we have full blown competition and to make sure that everybody in Europe can participate."," " )  
        translatedText = translatedText.replace("We need to make sure that we have full blown competition and to make sure that everybody in Europe can participate.", " ").replace("We need to make sure that we have full blown competition and to make sure that everybody in the supply chain can benefit.", " ").replace("We need to make sure that we have full blown competition and to make sure that European companies remain competitive on a global scale."," ")
        
        
         
           
    return translatedText


def textView(myStr="", targetLanguageCode="", sourceLanguageCode=""):

    
    
    try:
        if sourceLanguageCode == "auto":
            sourceLanguageCode =  checkLanguage(myStr.replace("\n"," ")[:200])
            print("Source",sourceLanguageCode)



    except Exception as e:
        return Response(
            {
                'status':status.HTTP_400_BAD_REQUEST,
                'response':"Source Language Detection Failed"
            }
        )  
          
    # Splitting Through Line
    sourceTextList = myStr.split(".")
    
    # print("--------->",sourceTextList)
    # Making Prediction
    output = makePrediction(
        sourceLanguageCode=sourceLanguageCode,
        sourceTextList=sourceTextList,
        targetLanguageCode=targetLanguageCode
        )
    
    return output

   

def extract_text_from_pdf(pdf_path, ocr_lang='en'):
  
    try:
        pdf_reader = PdfReader(pdf_path)
        reader = easyocr.Reader([ocr_lang],gpu = False)
        complete_text = ""
        pages_as_images = convert_from_path(pdf_path)
        for page in pages_as_images:
            osd_data = pytesseract.image_to_osd(page, config='--psm 0')
            


        for i, page in enumerate(pdf_reader.pages):
            extracted_text = page.extract_text()

            if extracted_text:
                complete_text += extracted_text + '\n'
            else:
                img_byte_array = io.BytesIO()
                pages_as_images[i].save(img_byte_array, format="PNG")
                result = reader.readtext(img_byte_array.getvalue())
                image_text = ' '.join([item[1] for item in result])
                complete_text += image_text + '\n'
                img_byte_array.close()

        return complete_text

    except Exception as e:
        print(f"Error: {e}")
        return str(e)
    

def extract_text_from_textFile(txt_path):
    textFile = open(txt_path, 'r')
    return textFile.read()

def extract_text_from_docx(doc_path):
    raw_text = docx2txt.process(doc_path)
    return raw_text

def extractTextFromFile(filePath=""):
    '''
        Check for PDF/text/docx
    '''
    path = str(settings.BASE_DIR)+filePath
    
    # Changing Path for windows/linux
    # path = path.replace("/","\\")

    fileExtension = path.split("/")[-1].split(".")[-1]
  
    if fileExtension =="pdf":
        completText = extract_text_from_pdf(path)
    elif fileExtension == "txt":
        completText = extract_text_from_textFile(path)
    elif fileExtension == "docx":
        completText = extract_text_from_docx(path)
   
    return completText
    


def fileView(filePath="",  targetLanguageCode="",  sourceLanguageCode=""):

    try:
        textFromFile = extractTextFromFile(filePath)
       
    except Exception as e:
         return Response(
            {
                'status':status.HTTP_400_BAD_REQUEST,
                'response':str(e)
            }
        )  

    response = textView(myStr=textFromFile, targetLanguageCode=targetLanguageCode, sourceLanguageCode=sourceLanguageCode)
    
    try:
        path = str(settings.BASE_DIR)+filePath
    
        os.remove(path)
        
    except Exception as e:
        print(str(e))
    
    return response
    
