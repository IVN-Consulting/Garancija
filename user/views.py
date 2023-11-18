from rest_framework import views, response, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomPermission(permissions.BasePermission):
    message = 'NE MOZE'
    def has_permission(self, request, view):
        return True

class MeView(generics.GenericAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, CustomPermission)

    def get(self, request):
        return response.Response({
            "id": request.user.id,
            "first_name": request.user.first_name,
            "last-name": request.user.last_name,
            "email": request.user.email,
            "phone_number": request.user.phone_number,
            "user_type": request.user.user_type,
            "permissions": request.user.get_all_permissions()
        })