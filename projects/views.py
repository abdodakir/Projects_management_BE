"""
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
import datetime
import json
from projects.models import *
from django.utils import timezone

def currentTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@require_http_methods(["POST"])
def student_singup(request):
    data = json.loads(request.body)
    kwargs = {}
    kwargs["st_created_date"] = currentTime()
    if "action" in data and data.get("action") == "create":
        if data.get("st_name") != None:
            kwargs["st_name"] = data.get("st_name")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("st_username") != None:
            kwargs["st_username"] = data.get("st_username")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("st_password") != None:
            kwargs["st_password"] = make_password(data.get("st_password"), salt=None, hasher='default')
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("st_email") != None:
            kwargs["st_email"] = data.get("st_email")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("st_school_year") != None:
            kwargs["st_school_year"] = data.get("st_school_year")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        if data.get("st_phone") != None:
            kwargs["st_phone"] = data.get("st_phone")
        else:
            return JsonResponse({"success": False, "message": "missing data!"}, safe=False)
        student = Student.objects.create(**kwargs)
        student.save()
        kwargs["student_id"]=student.id
        response = {
            "success": True,
            "data": kwargs
        }
        return JsonResponse(response, safe=False)
    return JsonResponse(response, safe=False)

@require_http_methods(["GET","POST"])
def student_singin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("**"*20)
        print(data)
        print("**"*20)
        return JsonResponse(data, safe=False)
    return JsonResponse({"success": False, "message": "Bed request"}, safe=False)

