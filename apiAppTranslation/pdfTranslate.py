import subprocess
import os
from .mlModel.Seamless_m4t_v2_large import translator
from rest_framework.response import Response
from rest_framework import status
from deep_translator import GoogleTranslator
from .languageCodes import getLanguageCode2To3
from .languageCodes import getLanguageCode3To2
from ftlangdetect import detect
from bs4 import BeautifulSoup
from django.conf import settings   
import pdfkit
import tempfile
from PyPDF2 import PdfReader
from pdf2image.pdf2image import convert_from_path
import pytesseract
import easyocr
import random
import re
import io
import requests
def is_connected_to_internet():
    try:
        # Try to send a GET request to a reliable website (e.g., google.com)
        response = requests.get("http://www.google.com", timeout=5)
        # If the request is successful and the status code is 200, the internet connection is available.
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

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
    sourceText="", 
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
    translatedText = translated_text.replace("We need to make sure that we have full blown competition and to make sure that everybody in Europe can participate."," " )  
    translatedText = translatedText.replace("We need to make sure that we have full blown competition and to make sure that everybody in Europe can participate.", " ").replace("We need to make sure that we have full blown competition and to make sure that everybody in the supply chain can benefit.", " ").replace("We need to make sure that we have full blown competition and to make sure that European companies remain competitive on a global scale."," ")
        
        
         
           
    return translatedText

def extract_text_from_pdf(pdf_path, ocr_lang='en'):
    print("->",pdf_path)
    try:
        pdf_reader = PdfReader(pdf_path)
        print("--->",pdf_reader)
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
    
def translate_pdf_to_pdf(input_pdf_file, source_language, target_language='es'):
    """
    Convert a PDF file to a translated PDF in the specified language.
    """

    def convert_pdf_to_html(pdf_path, html_path):
        print("ffffffff",pdf_path)
        """
        Convert a PDF file to an HTML file.
        """
        subprocess.run(["pdftohtml", "-s", "-p", pdf_path, html_path])
        return html_path.replace('.html', '-html.html')

    # Convert PDF to HTML
    if is_connected_to_internet():
        intermediate_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
        actual_html_file = convert_pdf_to_html(input_pdf_file, intermediate_html_file)
        source_language =  getLanguageCode3To2(languageCode=source_language)
        target_language =  getLanguageCode3To2(languageCode=target_language)
        print(source_language,target_language,"fffggh")
        translate = GoogleTranslator(source="auto", target=target_language)
        # Read the converted HTML
        with open(actual_html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Translate HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        texts = soup.find_all(text=True)

        for text in texts:
            if text.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                stripped_text = text.strip()
                if stripped_text:
                    try:
                        translated_text = translate.translate(stripped_text)
                        #translated_text = makePrediction(stripped_text,source_language,target_language)
                        text.replace_with(translated_text)
                    except Exception as e:
                        print(f"Error translating text: {e}")
                        continue
    else:
            intermediate_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
            actual_html_file = convert_pdf_to_html(input_pdf_file, intermediate_html_file)
            
            # Read the converted HTML
            with open(actual_html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Translate HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
            texts = soup.find_all(text=True)

            for text in texts:
                if text.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                    stripped_text = text.strip()
                    if stripped_text:
                        try:
                            translated_text = makePrediction(stripped_text,source_language,target_language)
                            text.replace_with(translated_text)
                        except Exception as e:
                            print(f"Error translating text: {e}")
                            continue
    # Inject CSS for print styling
    style_tag = soup.new_tag('style', type='text/css')
    style_tag.string = """
    body {
        font-family: sans-serif;
        overflow-wrap: break-word;
        word-wrap: break-word;
        word-break: break-word;
    }
    @media print {
        a::after {
            content: ' (' attr(href) ') ';
        }
        pre {
            white-space: pre-wrap;
        }
        @page {
            margin: 0.75in;
            size: Letter;
            @top-right {
                content: counter(page);
            }
        }
        @page :first {
            @top-right {
                content: '';
            }
        }
    }
    """
    soup.head.append(style_tag)

    # Temporary HTML file for translated content
    translated_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name

    # Save the translated HTML content
    with open(translated_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    # Convert the translated HTML to PDF
    output_pdf_file = "media/uploads/pdffile.pdf"
    pdfkit.from_file(translated_html_file, output_pdf_file, options={"enable-local-file-access": True})

    # Clean up temporary files
    os.remove(actual_html_file)
    os.remove(translated_html_file)

    return output_pdf_file


def Translatepdf(uploaded_file,source_language,target_language):
        
        try:
            translated_pdf = translate_pdf_to_pdf(uploaded_file,source_language, target_language)
            
            return translated_pdf
        except Exception as e:
            print(f"An error occurred: {e}")

        # Cleanup
        #os.remove(input_pdf_path)
        os.remove(translated_pdf)

def fileView(filePath="",  targetLanguageCode="", sourceLanguageCode=""):

    try:
        path = str(settings.BASE_DIR)+filePath
        sourceText = extract_text_from_pdf(path, ocr_lang='en')
        
        if sourceLanguageCode == "auto":
            sourceLanguageCode = checkLanguage(sourceText)

        response = Translatepdf(path,sourceLanguageCode,targetLanguageCode)
    
        path = str(settings.BASE_DIR)+filePath
    
        os.remove(path)
        
    except Exception as e:
        response=str(e)

    return response
