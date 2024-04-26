from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import SignUpForm,ClientSignUpForm
from .models import Job,Account
# Create your views here.
from django.contrib.auth.forms import AuthenticationForm

def index(request):

    return render(request,"index.html")
def dashboard(request):
    jobs=Job.objects.all()

    return render(request,'dashboard.html',{'jobs':jobs})


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
            return redirect('dashboard')  # veya başka bir sayfaya yönlendirme yapabilirsiniz
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
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/user_login.html', {'form': form})


def jobdetail(request,id):
    job=Job.objects.get(id=id)

    return render(request,'jobdetail.html',{'job':job})



