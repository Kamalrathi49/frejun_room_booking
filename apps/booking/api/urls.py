# third party imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path

# local imports
from apps.booking.api.views import BookingViewSet, RoomAvailabilityView, TeamViewSet, MemberViewSet

router = DefaultRouter()
router.register('', BookingViewSet, basename='booking')
router.register('teams', TeamViewSet, basename='team')
router.register('members', MemberViewSet, basename='member')

urlpatterns = [
    path('rooms/available/', RoomAvailabilityView.as_view(), name='room-available'),
]
urlpatterns += router.urls 