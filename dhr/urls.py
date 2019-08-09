from django.conf.urls import url, include
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls

from dhr.views import views
from dhr.views.authviews import obtain_jwt_token


router = routers.DefaultRouter()
router.register(r'users', views.UserView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(
        title='Project API',
        description='An API to interact with the Project App',
        permission_classes=[permissions.AllowAny],
    )),
    url(r'auth/login/', obtain_jwt_token),

]
