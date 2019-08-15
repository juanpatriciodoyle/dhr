from django.conf.urls import url, include
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls

from dhr.views import views
from dhr.views.authviews import obtain_jwt_token


router = routers.DefaultRouter()
router.register(r'users', views.UserView)
router.register(r'dockets', views.DocketView)
router.register(r'workShift', views.WorkShiftView)
router.register(r'weeklySchedule', views.WeeklyScheduleView)
router.register(r'familyMember', views.FamilyMemberView)
router.register(r'bank', views.BankView)
router.register(r'healthInsurance', views.HealthInsuranceView)
router.register(r'address', views.AddressView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(
        title='Project API',
        description='An API to interact with the Project App',
        permission_classes=[permissions.AllowAny],
    )),
    url(r'auth/login/', obtain_jwt_token),

]
