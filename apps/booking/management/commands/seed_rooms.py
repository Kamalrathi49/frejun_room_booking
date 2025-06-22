# django imports
from django.core.management.base import BaseCommand

# local imports
from apps.booking.models import Room

class Command(BaseCommand):
    help = 'Seed the database with default rooms'

    def handle(self, *args, **kwargs):
        data = [
            # 8 private
            *[
                {"name": f"Private Room {i+1}", "room_type": Room.PRIVATE, "capacity": 1}
                for i in range(8)
            ],
            # 4 conference
            *[
                {"name": f"Conference Room {i+1}", "room_type": Room.CONFERENCE, "capacity": 10}
                for i in range(4)
            ],
            # 3 shared desks
            *[
                {"name": f"Shared Desk {i+1}", "room_type": Room.SHARED, "capacity": 4}
                for i in range(3)
            ],
        ]

        created_count = 0
        for room_data in data:
            obj, created = Room.objects.get_or_create(name=room_data["name"], defaults=room_data)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} rooms'))
