from rest_framework import status
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken, JSONWebTokenAPIView
from dhr.serializers import CurrentUserSerializer
from dhr.utils import LogUtilMixin

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class MyObtainJSONWebToken(ObtainJSONWebToken, LogUtilMixin):

    def post(self, request, *args, **kwargs):
        response = super(MyObtainJSONWebToken, self).post(request, args, kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = UserModel.objects.get(username=request.data['username'])
            response.data['user'] = CurrentUserSerializer(user).data
        return response


class RefreshJSONWebToken(JSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = RefreshJSONWebTokenSerializer


obtain_jwt_token = MyObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
