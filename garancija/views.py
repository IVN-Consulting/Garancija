from rest_framework import views, response

class Healthcheck(views.APIView):
    def get(self, request):
        return response.Response("OK")