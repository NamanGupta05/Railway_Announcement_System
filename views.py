from django.shortcuts import render, HttpResponse
from datetime import datetime
from system.models import Contact
from django.contrib import messages
from railway.settings import BASE_DIR
from django.http import JsonResponse
import json
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

import googletrans
from googletrans import Translator # To detect and translate text
import speech_recognition as sr # To recognize speech
from gtts import gTTS # Google Text-to-Speech to convert text to audio
import os # To work with files
import pyttsx3

# Create your views here.

def home(request):
    return render(request, 'home.html',{'link' : 'index.html' ,})

def index(request):
    return render(request, 'index.html')

def index1(request):
    return render(request, 'index1.html')

def homebtn(request):
    return render(request, 'homebtn.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')


@csrf_exempt
def audio(request):
    json_data = json.loads(request.body)
    file = str(BASE_DIR) + "\\system\\hindi1.wav"
    r = sr.Recognizer()
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        audio = r.listen(source)
        rec_audio = r.recognize_google(audio)
        translator = Translator()
        new_text = translator.translate(rec_audio, src="hi", dest=json_data["lang"])
    return HttpResponse(new_text.text)

def speech(request):
    text = request.GET.get("text", "")
    speak = gTTS(text=text, lang=request.GET.get("lang", ""), slow=False)
    mp3 = BytesIO()
    speak.write_to_fp(mp3)
    response = HttpResponse()
    response.write(mp3.getvalue())
    response["Content-Type"] = "audio/mp3"
    return response