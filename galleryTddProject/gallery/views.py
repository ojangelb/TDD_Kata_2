from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as do_login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Image
import json


# Create your views here.

@csrf_exempt
def index(request):
    images_list = Image.objects.all()
    return HttpResponse(serializers.serialize("json", images_list))


@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        username = json_user['username']
        user_model = User.objects.filter(username=username)
        first_name = json_user['first_name']
        last_name = json_user['last_name']
        email = json_user['email']

        if len(user_model) ==0:
            password = json_user['password']
            username = json_user['username']
            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()
        else:
            User.objects.filter(username=username).update(first_name=first_name, last_name=last_name,
                                                          email=email)
            user_model = User.objects.filter(username=username).first()

    return HttpResponse(serializers.serialize("json", [user_model]))

@csrf_exempt
def portafolioFiltroPublico(request):
    user_name = request.GET.get('username')
    images_list = Image.objects.filter(user__username=user_name, isPublic=True)
    return HttpResponse(serializers.serialize("json", images_list))


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        password = jsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            message = username
        else:
            message = 'Nombre de usuario o contraseña incorrectos'

    return JsonResponse({"user": message})


