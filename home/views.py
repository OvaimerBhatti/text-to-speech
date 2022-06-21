
import email
import django
from django.conf import settings
from django.shortcuts import render,redirect
import pikepdf
from .models import Register
from gtts import gTTS
from pdf2image import convert_from_path
import os
from PIL import Image
from pytesseract import *
#download and install tesseract and put its desired location below
pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def signup_url(request):
        if request.method=='GET':
            return render(request, 'signup.html')
        else:
            postData= request.POST
            name=postData.get('name')
            email=postData.get('email')
            password=postData.get('password')
            sex=postData.get('sex')
            #validation
            value={
                'name' : name,
                'email' : email,
                'password' : password,
                'sex' : sex
            }
            error_message=None
            register= Register(name=name,
                                email=email,
                                password=password,
                                )
            if(not name):
                error_message="Name is Required !"
            elif len(name)<4:
                error_message="Name must be 4 char long or more !"
            elif(not email):
                error_message="Email is Required !"
            elif len(email)<4:
                error_message="Please put a valid email !"
            elif(not password):
                error_message="Password is Required !"
            elif len(password)<8:
                error_message="Password must be 8 char long or more !"
            elif(not sex):
                error_message="Gender is Required !"
            elif register.isExists():
                error_message="Already Registered Email.."
            #save
            if not error_message:
                

                register.upload()
                error_message="Account Registered Successfuly!"
                return render(request, 'signup.html', {'error':error_message})
                
            else:
                data = {
                    'error':error_message,
                    'values' : value
                }
                return render(request, 'signup.html', data)


def login_url(request):
        if request.method == 'GET':
            return render(request, 'login.html')
        else:
            email=request.POST.get('email')
            password=request.POST.get('password')
            register=Register.get_user(email,password)
            print(register)
            print(email,password)
            error_message=None
            if register:
                request.session['email'] = email
                return redirect('converter')
            else:
                error_message= 'Email or Password is invalid!'
            return render(request, 'login.html',{'error':error_message})


def converter_url(request):
    language = 'en'
    music = ''
    #it provides the functionality of pdf to text to speech conversion
    if request.method == 'POST' and request.FILES.get('pdf'):
        try:
            os.remove(f'static/file.pdf')
            error_message= 'There was an incomplete process! Now try again..'
            return render(request, 'converter.html',{'error':error_message})
        except:
            pdf = request.FILES['pdf']
            lang = request.POST.get('lang')
            try:
                with pikepdf.open(pdf) as pdf:
                    pdf.save("static/file.pdf")
            except:
                error_message= 'file type error! Please put a pdf file only'
                return render(request, 'converter.html',{'error':error_message})
            print("Decrpytion Completed!!")

            error_message=None
            if lang =='hin':
                language='hi'
            elif lang =='eng':
                language='en'
            elif lang == 'guj':
                language='gu'
            elif lang == 'chi_sim':
                language='zh'
            else:
                language='en'
            if pdf:
                pdfs = r"static/file.pdf"
                #download the poppler file from github and extract in C drive
                pages=convert_from_path(pdfs, 350, poppler_path=r"C:\poppler-0.68.0\bin")
                text=""
                i=1
                print(len(pages))
                
                # it converts page to image, fetches the data & then delete the image..& does this again
                for page in pages:
                    image_name="Page_" + str(i) + ".jpg"
                    page.save(f'static/uploads/{image_name}')
                    img=Image.open(f"static/uploads/{image_name}")
                    new_size= tuple(4*x for x in img.size)
                    img=img.resize(new_size, Image.ANTIALIAS)
                    output= pytesseract.image_to_string(img, lang=lang)
                    i = i+1
                    text += output
                    print(text)
                    os.remove(f'static/uploads/{image_name}')
                os.remove('static/file.pdf')

                #it converts the text into speech 
                try:
                    if text:
                        myobj = gTTS(text=text, lang=language, slow=False, )
                        myobj.save("static/speech.mp3")
                        music = 'ok'
                        context = {
                            'music': music,
                                    }
                        return render(request, 'converter.html', context)
                    else: 
                        error_message= 'There is no text in the pdf file!'
                        return render(request, 'converter.html',{'error':error_message})
                except:
                    error_message= 'Please check your internet connection and try again!'
                    return render(request, 'converter.html',{'error':error_message})

    # it provides functionality of image to text to speech conversion
    elif request.method == 'POST' and request.FILES.get('image'):
        picture = request.FILES['image']
        lang = request.POST.get('lang')
        try:
            with Image.open(picture) as png:
                png.save(f'static/image.png')
        except:
            error_message= 'File type error! please put jpg, jpeg or png image only'
            return render(request, 'converter.html',{'error':error_message})
        print("Image saved")  
        img=Image.open('static/image.png') 
        new_size= tuple(4*x for x in img.size)
        img=img.resize(new_size, Image.ANTIALIAS)
        output= pytesseract.image_to_string(img, lang=lang)
        print(output)
        if lang =='hin':
            language='hi'
        elif lang =='eng':
            language='en'
        elif lang == 'guj':
            language='gu'
        elif lang == 'chi_sim':
            language='zh'
        else:
            language='en'
        try:    
            if output:
                    myobj = gTTS(text=output, lang=language, slow=False, )
                    myobj.save("static/speech.mp3")
                    music = 'ok'
                    context = {
                        'music': music,
                                }
                    return render(request, 'converter.html', context)
            else:
                error_message= 'There is no text in the image file!'
                return render(request, 'converter.html',{'error':error_message})
        except:
            error_message= 'Please check your internet connection and try again!'
            return render(request, 'converter.html',{'error':error_message})
    elif request.method == 'POST':
        error_message="Please choose a file first!"
        return render(request, 'converter.html', {'error':error_message})
    else:
        print('you are : ', request.session.get('email'))
        return render(request, 'converter.html')


def logout_url(request):
    request.session.clear()
    return redirect('login')
    
    
