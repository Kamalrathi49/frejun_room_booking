# third party imports
from rest_framework import serializers

# local imports
from apps.booking.models import Booking, Room, Team, Member
from apps.users.models import User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['uuid', 'name', 'room_type', 'capacity', 'description']


class MemberSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(
        queryset=Team.objects.all(),
        slug_field='uuid',
        write_only=True,
        required=True
    )
    class Meta:
        model = Member
        fields = ['uuid', 'name', 'age', 'gender', 'email', 'team']
    

class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['uuid', 'name', 'description', 'members']


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    room_id = serializers.UUIDField(write_only=True, required=False)
    team_id = serializers.UUIDField(write_only=True, required=False)
    user_id = serializers.UUIDField(write_only=True, required=False)
    member_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)

    class Meta:
        model = Booking
        fields = [
            'id', 'uuid', 'room', 'room_id',
            'team', 'team_id', 'user_id', 'member_ids',
            'date', 'slot',
        ]
        read_only_fields = ['id', 'uuid', 'room', 'team', 'status']