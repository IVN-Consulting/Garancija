from rest_framework.views import APIView
from rest_framework.response import Response


class MyFirstEndpoint(APIView):
    def get(self, request):
        return Response("Hello from django rest framework")

