from rest_framework.views import APIView
from rest_framework.response import Response
from old_code.sync_resources import BackendAPI, FrontendAPI, Syncer


class MyFirstEndpoint(APIView):
    def get(self, request):
        return Response("Hello from django rest framework")

class Buda(APIView):
    def get(self, request):
        return Response("Hello from Buda")

class SyncerEndpoint(APIView):
    def get(self,request):
        group_workspaces = {
            'User Service': ['Authentication', 'User Management'],
            'Shop Service': ['Shop API'],
            'Warranty Service': ['Warranty API']
        }
        frontend = FrontendAPI(_type="myhome")
        backend = BackendAPI(_type="group", workspaces=group_workspaces, _filter=True)
        syncer = Syncer(backend=backend, frontend_api=frontend)
        workspaces = syncer.sync()

        return Response(workspaces)
