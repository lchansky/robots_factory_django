import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView


from robots.models import Robot


class API(APIView):
    def post(self, request):
        post_data = request.data
        try:
            robot = Robot.objects.create(**post_data)
        except ValidationError as e:
            return HttpResponseBadRequest(content=json.dumps(e.message_dict))

        robot_dict = robot.__dict__
        robot_dict.pop('_state')
        return Response(data=robot_dict)


