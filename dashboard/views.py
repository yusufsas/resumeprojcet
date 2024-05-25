from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import SignUpForm, ClientSignUpForm, ImageUploadForm, UserProfileForm
from .models import Job, Account, ImageUpload, UserProfile
from .serializers import JobSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import cv2
import os

import numpy as np
def index(request):
    return render(request, "index.html")
def dashboard(request):
    if request.user.is_authenticated:

        user_role = request.user.account.role

        if user_role == Account.ROLE_ADMIN:
            jobs = Job.objects.all()
            accounts=Account.objects.all()
           
        
            user = request.user.id
            account = Account.objects.get(user_id=user)
           
            if request.method == 'POST':

                if 'form1_submit' in request.POST:
                    image = request.FILES.get("resim")
                    output_path = yuz_algila(image)
                    image_path = os.path.join(settings.MEDIA_ROOT, str(account.image))
                    #output_path = detect_faces(image_path)
                 
                    
                    if output_path:
                        account.image = image
                        account.save()
                        return render(request, 'dashboard.html', {'jobs': jobs,'account':account,'accounts':accounts})
                    else:
                      
                        message = "Yüzünüzün bulunduğu bir fotoğraf yükleyiniz"
                        return render(request, 'dashboard.html', {'jobs': jobs,  'message': message,'account':account,'accounts':accounts})
                elif 'form2_submit' in request.POST:
            
                    cv = request.FILES.get("pdf_file")
                    account.cv = cv
                    account.save() 
            return render(request, 'dashboard.html', {'jobs': jobs,'account':account,'accounts':accounts})

            # Admin için tüm görevleri listele
        elif user_role == Account.ROLE_MANAGER:
            jobs = Job.objects.all()
        
            user = request.user.id
            account = Account.objects.get(user_id=user)
           
            if request.method == 'POST':

                if 'form1_submit' in request.POST:
                    image = request.FILES.get("resim")
                    output_path = yuz_algila(image)
                    image_path = os.path.join(settings.MEDIA_ROOT, str(account.image))
                    #output_path = detect_faces(image_path)
                 
                    
                    if output_path:
                        account.image = image
                        account.save()
                        return render(request, 'dashboard.html', {'jobs': jobs,'account':account})
                    else:
                      
                        message = "Yüzünüzün bulunduğu bir fotoğraf yükleyiniz"
                        return render(request, 'dashboard.html', {'jobs': jobs,  'message': message,'account':account})
              
                elif 'form2_submit' in request.POST:
            
                    cv = request.FILES.get("pdf_file")
                    account.cv = cv
                    account.save()

                elif 'addjob' in request.POST:

                    job_name=request.POST.get('name')
                    des=request.POST.get('description')
                    instance=Job.objects.create(name=job_name,description=des)
                    instance.save()

            
        elif user_role == Account.ROLE_EMPLOYEE:
            jobs = Job.objects.all()
        
            user = request.user.id
            account = Account.objects.get(user_id=user)
           
            if request.method == 'POST':

                if 'form1_submit' in request.POST:
                    image = request.FILES.get("resim")
                    output_path = yuz_algila(image)
                    image_path = os.path.join(settings.MEDIA_ROOT, str(account.image))
                    #output_path = detect_faces(image_path)
                 
                    
                    if output_path:
                        account.image = image
                        account.save()
                        return render(request, 'dashboard.html', {'jobs': jobs,'account':account})
                    else:
                      
                        message = "Yüzünüzün bulunduğu bir fotoğraf yükleyiniz"
                        return render(request, 'dashboard.html', {'jobs': jobs,  'message': message,'account':account})
                elif 'form2_submit' in request.POST:
            
                    cv = request.FILES.get("pdf_file")
                    account.cv = cv
                    account.save()

        
            
    return render(request, 'dashboard.html', {'jobs': jobs,'account':account})
def delete_account(request, id):
    account = Account.objects.get(id=id)
    account.delete()
    return redirect('dashboard')


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        client_form = ClientSignUpForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = SignUpForm()
        client_form = ClientSignUpForm()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'client_form': client_form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/user_login.html', {'form': form})

def jobdetail(request, id):
    job = Job.objects.get(id=id)
    return render(request, 'jobdetail.html', {'job': job})


def yuz_algila(image):
    # OpenCV kullanarak yüz algılama işlemi
    yuz_cascadesi = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Django'nun imagefield'ı doğrudan bir dosya yoluna işaret etmez, bu yüzden önce bir image dosyasına çevirmemiz gerekiyor
    # Örneğin, bu işlem için PIL (Python Imaging Library) veya OpenCV kütüphanelerini kullanabilirsiniz.
    
    # PIL kullanarak:
    # image_data = Image.open(image)
    # fotograf = np.array(image_data)
    
    # OpenCV kullanarak:
    fotograf = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Gri tonlamaya dönüştür
    gri_tonlama = cv2.cvtColor(fotograf, cv2.COLOR_BGR2GRAY)
    
    # Yüzleri tespit et
    yuzler = yuz_cascadesi.detectMultiScale(gri_tonlama, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Eğer yüz bulunduysa True, bulunamadıysa False döndür
    if len(yuzler) > 0:
        return True
    else:
        return False
    
    
def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    found_faces = False
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        found_faces = True
    
    output_path = os.path.join('images', 'detected_faces.jpg')  # 'settings.MEDIA_ROOT' ayarlanmamışsa kullanılamaz
    cv2.imwrite(output_path, img)
    
    return found_faces

def upload_image(request):
    user = request.user.id
    account = Account.objects.get(user_id=user)
    if request.method == 'POST':
        image = request.FILES.get("img")
        account.image = image
        account.save()
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', str(account.image))
        output_path = detect_faces(image_path)
        image = ImageUpload.objects.all().first()
        return render(request, 'face_detection/result.html', {'output_path': output_path, 'image': image})
    
    return render(request, 'face_detection/upload.html')


def show_detected_face(request):
    output_path = os.path.join(settings.MEDIA_ROOT, 'images', 'detected_faces.jpg')
    if os.path.exists(output_path):
        image_url = os.path.join(settings.MEDIA_URL, 'images', 'detected_faces.jpg')
    else:
        image_url = None
    return render(request, 'show_detected_face.html', {'image_url': image_url})

from django.shortcuts import render, redirect
from django.urls import reverse

def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile_picture_path = os.path.join(settings.MEDIA_ROOT, profile.profile_picture.name)
            if not detect_faces(profile_picture_path):
                form.add_error('profile_picture', 'Yüzünüzün açık olduğu bir fotoğraf koyunuz.')
                return render(request, 'profiles/update_profile.html', {'form': form})
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profiles/update_profile.html', {'form': form})


def pdf_view(request):
    user = request.user.id
    account = Account.objects.get(user_id=user)

    pdf = account.cv
    with open(pdf.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
    return response

def search_jobs(request):
    query = request.POST.get('q', '')
    if query:
        jobs = Job.objects.filter(name__icontains=query)
        return render(request, 'search_jobs.html', {'jobs': jobs})
    return render(request, 'search_jobs.html', {'jobs': []})


class SearchJobsAPI(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            jobs = Job.objects.filter(name__icontains=query)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    