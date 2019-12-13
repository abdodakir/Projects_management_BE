"""
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
import datetime
import json
from projects.models import *

def currentTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@require_http_methods(["POST"])
def register(request):
    data = json.loads(request.body)
    kwargs = {}
    kwargs["p_created_date"] = currentTime()
    if "action" in data and data.get("action") == "create":
        if data.get("p_name") != None:
            kwargs["p_name"] = data.get("p_name")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("p_username") != None and not User.objects.filter(p_username=data.get("p_username")).exists():
            kwargs["p_username"] = data.get("p_username")
        else:
            return JsonResponse({"success": False, "message": "Username already exist!"}, safe=False)
        if data.get("p_password") != None:
            kwargs["p_password"] = make_password(data.get("p_password"), salt=None, hasher='default')
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("p_email") != None:
            kwargs["p_email"] = data.get("p_email")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("p_school_year") != None:
            kwargs["p_school_year"] = data.get("p_school_year")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("p_phone") != None:
            kwargs["p_phone"] = data.get("p_phone")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("p_phone") != None:
            kwargs["p_phone"] = data.get("p_phone")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        user = User.objects.create(**kwargs)
        user.save()
        kwargs["student_id"] = user.id
        response = {
            "success": True,
            "data": kwargs
        }
        return JsonResponse(response, safe=False)
    return JsonResponse({"success": False, "message": "missed Action!"}, safe=False)

@require_http_methods(["GET","POST"])
def login(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        if data.get("p_username") != None and User.objects.filter(p_username=data.get("p_username")).exists():
            user = User.objects.filter(p_username=data.get("p_username")).values()
            if check_password(data.get("p_password"), user[0]["p_password"]):
                return JsonResponse({"success": True, "user": list(user)}, safe=False)
            else:
                return JsonResponse({"success": False, "message": "wrong username or password!"}, safe=False)    
        else:
            return JsonResponse({"success": False, "message": "wrong username or password!"}, safe=False)
    return JsonResponse({"success": False, "message": "Bed request"}, safe=False)

@require_http_methods(["POST"])
def create_classes(request):
    data = json.loads(request.body)
    kwargs = {}
    if request.method == 'POST':
        kwargs["cl_created_year"] = currentTime()
        if data.get("cl_name", None) != None:
            kwargs["cl_name"] = data.get("cl_name")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("cl_cycle", None) != None:
            kwargs["cl_cycle"] = data.get("cl_cycle")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        classe = Classe.objects.create(**kwargs)
        classe.save()
        kwargs["classe_id"] = classe.id
        response = {
            "success": True,
            "data": kwargs
        }
        return JsonResponse(response, safe=False)
    return JsonResponse({"success": False, "message": "Bed request"}, safe=False)

@require_http_methods(["GET"])
def get_classes(request):
    data = json.loads(request.body)
    if request.method == 'GET':
        if data.get("action", None) == "get_classes":
            classes = Classe.objects.filter().values()
            response = {
                "success": True,
                "data": list(classes)
            }
        return JsonResponse(response, safe=False)
    return JsonResponse({"success": False, "message": "Bed request"}, safe=False)

@require_http_methods(["POST"])
def create_group(request):
    data = json.loads(request.body)
    kwargs = {}
    if request.method == 'POST':
        kwargs["created_date"] = currentTime()
        if data.get("gr_name", None) != None:
            kwargs["gr_name"] = data.get("gr_name")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("student_nbr", None) != None:
            kwargs["gr_student_nbr"] = data.get("student_nbr")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("school_year", None) != None:
            kwargs["gr_school_year"] = data.get("school_year")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("student_id", None) != None and User.objects.filter(id=data.get("student_id")).exists():
            kwargs["gr_created_by"] = data.get("student_id")
        else:
            return JsonResponse({"success": False, "message": "User doesn't existe!"}, safe=False)
        kwargs["gr_validated"] = False
        group = Group.objects.create(**kwargs)
        group.save()
        kwargs["group_id"] = group.id
        response = {
            "success": True,
            "data": kwargs
        }
        return JsonResponse(response, safe=False)
    return JsonResponse({"success": False, "message": "Bed request"}, safe=False)

@require_http_methods(["GET"])
def get_groups(request):
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
        return JsonResponse(response, safe=False)
    return JsonResponse({"success": False, "message": "Bed request"}, safe=False)

