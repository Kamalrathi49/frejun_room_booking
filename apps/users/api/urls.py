# third party imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

# local imports
from apps.users.api.views import UserAuthViewSet, UserDetailViewset


router = DefaultRouter()
router.register('auth', UserAuthViewSet, basename='user-auth')

urlpatterns = [
    path('', UserDetailViewset.as_view(), name='user-detail-update'),
    path('', include(router.urls)),
]