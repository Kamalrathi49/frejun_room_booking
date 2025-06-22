# third party imports
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# django imports
from django.db import transaction
from django.db.models import Q, Count

# std imports
from datetime import datetime, time

# local imports
from apps.booking.models import Booking, Room, Team, Member
from apps.users.models import User
from apps.booking.api.serializers import BookingSerializer, RoomSerializer, TeamSerializer, MemberSerializer

BOOKING_SLOTS = [time(h, 0) for h in range(9, 18)]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        team_uuid = self.request.query_params.get('team')
        if team_uuid:
            queryset = queryset.filter(team__uuid=team_uuid)
        return queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BookingViewSet(viewsets.ViewSet):
    """Handles booking, cancel, and list."""
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    
    
    def list(self, request):
        bookings = Booking.objects.select_related('room', 'team', 'user').filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request):
        data = request.data.copy()
        slot = data.get('slot')
        date_str = data.get('date')
        room_id = data.get('room_id')
        team_id = data.get('team_id')
        
        # Validate slot
        try:
            slot_time = datetime.strptime(slot, '%H:%M:%S').time()
            if slot_time not in BOOKING_SLOTS:
                return Response({'detail': 'Invalid slot.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'detail': 'Invalid slot format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate date
        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            return Response({'detail': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)
       
        # Validate room
        try:
            room = Room.objects.get(uuid=room_id)
        except Room.DoesNotExist:
            return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Booking logic by room type
        if room.room_type == Room.PRIVATE:
            # Only one user per slot
            if Booking.objects.filter(room=room, date=booking_date, slot=slot_time).exists():
                return Response({'detail': 'No available room for the selected slot and type.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Prevent user double-booking
            if Booking.objects.filter(date=booking_date, slot=slot_time, user=request.user).exists():
                return Response({'detail': 'User already has a booking for this slot.'}, status=400)
           
            booking = Booking.objects.create(room=room, date=booking_date, slot=slot_time, user=request.user)
            return Response({'booking_id': str(booking.uuid)}, status=status.HTTP_201_CREATED)
       
        elif room.room_type == Room.CONFERENCE:
            # Team booking, team size >= 3 (excluding children for seat, but included in headcount)
            if not team_id:
                return Response({'detail': 'Team required for conference room.'}, status=status.HTTP_400_BAD_REQUEST)
           
            try:
                team = Team.objects.get(uuid=team_id)
            except Team.DoesNotExist:
                return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            members = Member.objects.filter(team=team)
            if members.count() < 3:
                return Response({'detail': 'Conference room requires at least 3 team members.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Prevent double-booking for team
            if Booking.objects.filter(room=room, date=booking_date, slot=slot_time).exists():
                return Response({'detail': 'No available room for the selected slot and type.'}, status=status.HTTP_400_BAD_REQUEST)
            if Booking.objects.filter(date=booking_date, slot=slot_time, team=team).exists():
                return Response({'detail': 'Team already has a booking for this slot.'}, status=status.HTTP_400_BAD_REQUEST)
           
            booking = Booking.objects.create(room=room, team=team, date=booking_date, slot=slot_time, user=request.user)
            return Response({'booking_id': str(booking.uuid)}, status=status.HTTP_201_CREATED)
       
        elif room.room_type == Room.SHARED:
            # Shared desk: up to 4 users per slot
            # Find or create a booking for this slot/room with < 4 users
            existing_bookings = Booking.objects.filter(room=room, date=booking_date, slot=slot_time)
            if existing_bookings.count() >= room.capacity:
                return Response({'detail': 'No available room for the selected slot and type.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Prevent user double-booking
            if Booking.objects.filter(date=booking_date, slot=slot_time, user=request.user).exists():
                return Response({'detail': 'User already has a booking for this slot.'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking = Booking.objects.create(room=room, date=booking_date, slot=slot_time, user=request.user)
            return Response({'booking_id': str(booking.uuid)}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Invalid room type.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, uuid=None):
        try:
            booking = Booking.objects.get(uuid=uuid)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=404)
        booking.delete()
        return Response({'detail': 'Booking cancelled.'}, status=200)

class RoomAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        date_str = request.query_params.get('date')
        slot = request.query_params.get('slot')
       
        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        except Exception:
            return Response({'detail': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            slot_time = datetime.strptime(slot, '%H:%M:%S').time() if slot else None
        except Exception:
            return Response({'detail': 'Invalid slot format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        rooms = Room.objects.all()
        available = []
        for room in rooms:
            if booking_date and slot_time:
                count = Booking.objects.filter(room=room, date=booking_date, slot=slot_time).count()
                if room.room_type == Room.SHARED:
                    if count < room.capacity:
                        available.append(RoomSerializer(room).data)
                else:
                    if count == 0:
                        available.append(RoomSerializer(room).data)
            else:
                available.append(RoomSerializer(room).data)
        return Response(available) 