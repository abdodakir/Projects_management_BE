"""
    This is the views for the projects management. Some of them are good coded and others are badly codedv due to the time offered for this project. So they are coded just to work.
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
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    To update the Field of the user.
    """
    data = json.loads(request.body)
    if request.method == 'POST':
        kwargs = {}
        if data.get("username", None) == None or data.get("user_id", None) == None:
            return Response({"success": False, "message": "User Doesn't exist!"}, status=HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=data.get("username")).exists():
            return Response({"success": False, "message": "Username already exist!"}, status=HTTP_400_BAD_REQUEST)
        # I should improve it
        # create  the Object with values
        # 
        if data.get("firstname", None) != None:
            kwargs["first_name"] = data.get("firstname")
        if data.get("username", None) != None:
            kwargs["username"] = data.get("username")
        if data.get("lastname", None) != None:
            kwargs["last_name"] = data.get("lastname")
        if data.get("email", None) != None:
            kwargs["email"] = data.get("email")
        try:
            User.objects.filter(id=data.get("user_id")).update(**kwargs)
        except Users.DoesNotExist:
            return Response({"success": False, "message": "Update failed!"}, status=501)
        
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
            users = Users.objects.filter(user_id=data.get("user_id")).update(**kwargs)
        except Users.DoesNotExist:
            return Response({"success": False, "message": "Update failed!"}, status=501)
        
        # should be a function
        # Start
        user = User.objects.filter(id=data.get("user_id")).values()[0]
        users = Users.objects.filter(user_id=user["id"]).values()[0]
        token = Token.objects.filter(user_id=user["id"]).values()[0]
        
        users["first_name"] = user["first_name"]
        users["last_name"] = user["last_name"]
        users["username"] = user["username"]
        users["email"] = user["email"]
        users["last_login"] = user["last_login"]
        # End
        response = {"success": True, "token": token["key"], "user": users}
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)
    pass

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
                # End
                return Response({"success": True, "token": token.key, "user": users}, status=HTTP_200_OK)
            else:
                return Response({"success": False, "message": "wrong username or password 1!"}, status=HTTP_400_BAD_REQUEST)    
        else:
            return Response({"success": False, "message": "wrong username or password 2!"}, status=HTTP_400_BAD_REQUEST)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)

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
            return Response({"success": False, "message": "missing data!"}, status=HTTP_400_BAD_REQUEST)
        if data.get("cl_cycle", None) != None:
            kwargs["cl_cycle"] = data.get("cl_cycle")
        else:
            return Response({"success": False, "message": "missing data!"}, status=HTTP_400_BAD_REQUEST)
        classe = Classe.objects.create(**kwargs)
        classe.save()
        kwargs["classe_id"] = classe.id
        response = {
            "success": True,
            "data": kwargs
        }
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)

# This is a good one
@api_view(["GET"])
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
        return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)
    return Response({"success": True, "message": "loged out successfully"}, status=HTTP_200_OK)


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
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)

# This is a good one
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_group(request):
    """
    create groups by students 
    """
    data = json.loads(request.body)
    if request.method == 'POST':
        data["gr_created_date"] = currentTime()
        data["gr_validated"] = False
        try:
            user = Users.objects.get(id=data.get("gr_created_by"))
            group = Group()
            group.gr_created_by = user
            result = group.create_groupe(**data)
        except Group.DoesNotExist:
            return Response({"success": False, "message": "Create Group failed"}, status=HTTP_400_BAD_REQUEST)
        response = { "success": True, "data": result.to_dict() }
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)

# This is a good one
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_group(request):
    """
    create groups by students
    """
    data = json.loads(request.body)
    if request.method == 'POST':
        try:
            group = Group.objects.get(id=data.get("gr_id")).delete()
        except Group.DoesNotExist:
            return Response({"success": False, "message": "Delete Group failed"}, status=HTTP_400_BAD_REQUEST)
        response = { "success": True, "data": group }
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)

# This
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_group(request):
    """
    create groups by students 
    """
    data = json.loads(request.body)
    if request.method == 'POST':
        if not Group.objects.filter(id=data.get("gr_id")).exists():
            return Response({"success": False, "message": "Create Group failed"}, status=HTTP_400_BAD_REQUEST)
        try:
            group = Group.objects.filter(id=data.get("gr_id")).values()[0]
            gr_name = data["gr_name"] if "gr_name" in data else group["gr_name"]
            gr_student_nbr = data["gr_student_nbr"] if "gr_student_nbr" in data else group["gr_student_nbr"]
            Group.objects.filter(id=data.get("gr_id")).update(gr_name=gr_name, gr_student_nbr=gr_student_nbr)
            result = Group.objects.filter(id=data.get("gr_id")).values()[0]
        except Group.DoesNotExist:
            return Response({"success": False, "message": "Create Group failed"}, status=HTTP_400_BAD_REQUEST)
        response = { "success": True, "data": result }
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)

# This is a good one
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_groups(request):
    """
    get the groups created & apply a filter on them.
    """
    data = json.loads(request.body)
    kwargs = {}
    response = {}
    if request.method == 'GET':
        if data.get("action", None) == "get_groups":
            kwargs = data.get('data')  
            groups = Group.objects.filter(**kwargs).values()
            response = {
                "success": True,
                "data": list(groups)
            }
        return Response(response, status=HTTP_200_OK)
    return Response({"success": False, "message": "Bed request"}, status=HTTP_400_BAD_REQUEST)
