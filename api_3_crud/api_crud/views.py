from django.shortcuts import render
import io
import json

from rest_framework.parsers import JSONParser
from .models import Student
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# function based crud application
@csrf_exempt
def student_api(request):  # sourcery skip: avoid-builtin-shadow

    if request.method == 'GET':
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print(type(pythondata))
        id = pythondata.get('id', None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        stu = Student.objects.all()
        print(stu[0])
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(
            data=pythondata)  # variable name can by any
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data created'}
            # json_data = json.dumps(res)
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().renderer(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        # complete update
        # serializer = StudentSerializer(stu, data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'data updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {'msg': 'data deleted'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')
