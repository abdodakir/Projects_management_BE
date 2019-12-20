"""

"""
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import ( HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK )
from rest_framework.response import Response

import datetime
import json

from projects.models import *
from django.contrib.auth.models import User

def currentTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    """
    User register: check if the user exist if not create the new one using User model of Django extending to Users.
    - check that the required params exist 
    - select just the required params to avoid errors
    """
    data = json.loads(request.body)
    kwargs = {}
    kwargs["date_joined"] = currentTime()
    kwargs["last_login"] = currentTime()
    
    if "action" in data and data.get("action") == "create":
        user = ""
        if data.get("username", None) == None or User.objects.filter(username=data.get("username")).exists():
            return Response({"success": False, "message": "Username already exist!"}, status=HTTP_400_BAD_REQUEST)
        # This should be in function in models.py under the class Users
        # begin
        kwargs["username"] = data.get("username")
        
        if data.get("firstname", None) != None:
            kwargs["first_name"] = data.get("firstname")
        if data.get("password", None) != None:
            kwargs["password"] = data.get("password")
        if data.get("lastname", None) != None:
            kwargs["last_name"] = data.get("lastname")
        if data.get("email", None) != None:
            kwargs["email"] = data.get("email")
        try:
            user = User.objects.create_user(**kwargs)
            user.save()
        except User.DoesNotExist:
            return Response({"success": False, "message": "Username already exist!"}, status=HTTP_400_BAD_REQUEST)
        kwargs = {}
        
        if data.get("phone", None) != None:
            kwargs["p_phone"] = data.get("phone")
        if data.get("city", None) != None:
            kwargs["p_city"] = data.get("city")
        if data.get("country", None) != None:
            kwargs["p_country"] = data.get("country")
        if data.get("gender", None) != None:
            kwargs["p_gender"] = data.get("gender")
        if data.get("zip") != None:
            kwargs["p_zip"] = data.get("zip")
        
        try:
            users = Users.objects.create(user=user, **kwargs)
            users.save()
        except User.DoesNotExist:
            return Response({"success": False, "message": "Singup failed!"}, status=501)
        # End
        response = {
            "success": True,
            "message": "you have been registered successfully"
        }
        return Response(response)
    return Response({"success": False, "message": "missed Action!"}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    User login: check that the username exist and the password correct
    - create token authentication 
    - return the data of user
    """
    data = json.loads(request.body)
    if request.method == 'POST':
        if data.get("username", None) != None and User.objects.filter(username=data.get("username")).exists():
            user = User.objects.filter(username=data.get("username")).values()[0]
            #For debuging: import pdb; pdb.set_trace()
            if check_password(data.get("password"), user["password"]):
                user = authenticate(username=data.get("username"), password=data.get("password"))
                if not user:
                    return Response({"success": False, "user": user})
                token, _ = Token.objects.get_or_create(user=user)
                users = Users.objects.filter(user_id=user.id).values()[0]
                # should be a function
                # Start
                users["first_name"] = user.first_name
                users["last_name"] = user.last_name
                users["username"] = user.username
                users["email"] = user.email
                users["last_login"] = user.last_login
                del users["p_type"]
                # End
                return Response({"success": True, "token": token.key, "user": users}, status=HTTP_200_OK)
            else:
                return Response({"success": False, "message": "wrong username or password 1!"}, status=401)    
        else:
            return Response({"success": False, "message": "wrong username or password 2!"}, status=401)
    return Response({"success": False, "message": "Bed request"}, status=500)

# we don't need this, it's created manually by admin
@api_view(["POST"])
def create_classes(request):
    data = json.loads(request.body)
    kwargs = {}
    if request.method == 'POST':
        kwargs["cl_created_year"] = currentTime()
        if data.get("cl_name", None) != None:
            kwargs["cl_name"] = data.get("cl_name")
        else:
            return Response({"success": False, "message": "missing data!"})
        if data.get("cl_cycle", None) != None:
            kwargs["cl_cycle"] = data.get("cl_cycle")
        else:
            return Response({"success": False, "message": "missing data!"})
        classe = Classe.objects.create(**kwargs)
        classe.save()
        kwargs["classe_id"] = classe.id
        response = {
            "success": True,
            "data": kwargs
        }
        return Response(response)
    return Response({"success": False, "message": "Bed request"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    User logout: to destroy the token authentication
    - delete the token from database by selection the Id of the user 
    """
    data = json.loads(request.body)
    try:
        Token.objects.filter(user_id=data["user_id"]).delete()
    except KeyError:
        return Response({"success": False, "message": "Bed request"}, status=500)
    return Response({"success": True, "message": "loged out successfully"}, status=500)

@api_view(["GET"])
def get_classes(request):
    data = json.loads(request.body)
    kwargs = {}
    if request.method == 'GET':
        if data.get("action", None) == "get_classes":
            if data.get("data", None) != None:
                kwargs = data.get("data")

            classes = Classe.objects.filter(**kwargs).values()
            response = {
                "success": True,
                "data": list(classes)
            }
        return Response(response)
    return Response({"success": False, "message": "Bed request"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_group(request):
    """
    create groups by students 
    """
    data = json.loads(request.body)
    if request.method == 'POST':
        kwargs = data
        kwargs["created_date"] = currentTime()
        kwargs["gr_validated"] = False
        try:
            group = Group.objects.create(**kwargs)
            group.save()
            kwargs["group_id"] = group.id
        except Group.DoesNotExist:
            return Response({"success": False, "message": "Create Group failed"}, status=500)
        response = {
            "success": True,
            "data": kwargs
        }
        return Response(response)
    return Response({"success": False, "message": "Bed request"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_data(request):
    data = {"test": "this that just for test!"}
    return Response({"success": True, "message": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_groups(request):
    """
    get the groups created & apply a filter on them.
    """
    data = json.loads(request.body)
    kwargs = {}
    if request.method == 'GET':
        if data.get("action", None) == "get_groups":
            kwargs = data.get('data')  
            groups = Group.objects.filter(**kwargs).values()
            response = {
                "success": True,
                "data": list(groups)
            }
        return Response(response)
    return Response({"success": False, "message": "Bed request"})

