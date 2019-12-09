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
    return JsonResponse(response, safe=False)

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

