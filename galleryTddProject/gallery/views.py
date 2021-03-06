from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as do_login
from django.forms import model_to_dict
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

        if len(user_model) == 0:
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


@csrf_exempt
def edit_images_view(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        images = json_user['images']
        modified = []
        for img in images:
            img_model = Image.objects.filter(name=img['name']).first()
            if img_model is not None:
                img_model.isPublic = img['isPublic']
                img_model.save()
                modified.append(img_model)

    return HttpResponse(serializers.serialize("json", modified))

@csrf_exempt
def add_image_view(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        name = json_user['name']
        image_model = Image.objects.filter(name=name)
        username = json_user['user']['username']
        user_model = User.objects.filter(username=username).first()
        if len(image_model) == 0 and user_model is not None:
            image_model = Image()
            image_model.url = json_user['url']
            image_model.description = json_user['description']
            image_model.type = json_user['type']
            image_model.user = user_model
            image_model.isPublic = json_user['isPublic']
            image_model.save()
    return HttpResponse(serializers.serialize("json", Image.objects.filter(user__username=user_model)))
